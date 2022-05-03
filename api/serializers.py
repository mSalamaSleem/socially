from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Post


class AllPostsSerializer(serializers.ModelSerializer):
    # created_at = serializers.ReadOnlyField()
    # user = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'caption', 'user', 'created_at')
        read_only_fields = ('user', 'created_at')
