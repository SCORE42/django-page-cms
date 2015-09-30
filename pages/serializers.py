from pages.models import Page, Content
from rest_framework import serializers
from django.contrib.auth.models import User

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content

class PageSerializer(serializers.ModelSerializer):
    content_set = ContentSerializer(many=True, read_only=True)
    creation_date = serializers.DateTimeField()

    class Meta:
        model = Page

    def create(self, validated_data):

        attributes = ('status', 'delegate_to', 'freeze_date', 'creation_date',
            'publication_end_date', 'template', 'redirect_to_url',
            'last_modification_date', 'publication_date')

        admin = User.objects.filter(is_superuser=True)[0]

        cleaned_data = {}
        for attribute in attributes:
            cleaned_data[attribute] = validated_data.get(attribute)

        if validated_data.get('parent', False):
            cleaned_data['parent'] = validated_data.get('parent')

        cleaned_data['author'] = admin

        page = Page.objects.create(**cleaned_data)
        page.invalidate()
        return page