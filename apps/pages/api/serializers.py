from rest_framework import serializers

from apps.pages.models import StaticPage


class StaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPage
        fields = ['title', 'slug', 'content', 'image', 'meta_title',
                  'meta_description', 'created_at', 'updated_at']

