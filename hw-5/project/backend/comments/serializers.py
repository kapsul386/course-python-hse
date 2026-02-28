from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Comment, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_active"]


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "created_at",
            "likes_count",
            "comments_count",
        ]


class CommentSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at", "likes_count"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"