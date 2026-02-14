from django.contrib.auth.models import User
from django.db.models import Count, Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        return (
            Post.objects.all()
            .annotate(likes_count=Count("like", filter=Q(like__post__isnull=False)))
        )

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        post = self.get_object()
        Like.objects.get_or_create(user=request.user, post=post, comment=None)
        return Response({"status": "liked"}, status=status.HTTP_200_OK)

    @like.mapping.delete
    def unlike(self, request, pk=None):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        post = self.get_object()
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({"status": "unliked"}, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return (
            Comment.objects.all()
            .annotate(likes_count=Count("like", filter=Q(like__comment__isnull=False)))
        )

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        comment = self.get_object()
        Like.objects.get_or_create(user=request.user, comment=comment, post=None)
        return Response({"status": "liked"}, status=status.HTTP_200_OK)

    @like.mapping.delete
    def unlike(self, request, pk=None):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        comment = self.get_object()
        Like.objects.filter(user=request.user, comment=comment).delete()
        return Response({"status": "unliked"}, status=status.HTTP_200_OK)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
