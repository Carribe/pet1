from rest_framework import serializers

from .models import Page


class PagesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    class Meta:
        model = Page
        fields = ("title", "content", "belong_to", "slug", "user")
