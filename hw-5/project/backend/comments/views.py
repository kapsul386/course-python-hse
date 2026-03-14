from django.contrib.auth.models import User
from django.db.models import Count, Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Post, Comment, Like
from .permissions import IsAuthorOrReadOnly, IsSelfOrAdmin
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsSelfOrAdmin()]
        return [IsAuthenticated()]


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        return (
            Post.objects.all()
            .annotate(
                likes_count=Count(
                    "like",
                    filter=Q(like__post__isnull=False),
                    distinct=True,
                ),
                comments_count=Count("comments", distinct=True),
            )
            .order_by("-id")
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        Like.objects.get_or_create(user=request.user, post=post, defaults={"comment": None})
        return Response({"status": "liked"}, status=status.HTTP_200_OK)

    @like.mapping.delete
    def unlike(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        post = self.get_object()
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({"status": "unliked"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def top(self, request):
        """
        Top posts by likes.
        GET /api/posts/top/
        """
        qs = (
            Post.objects.all()
            .annotate(
                likes_count=Count("like", filter=Q(like__post__isnull=False), distinct=True)
            )
            .order_by("-likes_count", "-id")[:10]
        )
        data = [{"id": p.id, "title": p.title, "likes_count": p.likes_count} for p in qs]
        return Response(data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        return (
            Comment.objects.all()
            .annotate(
                likes_count=Count(
                    "like",
                    filter=Q(like__comment__isnull=False),
                    distinct=True,
                )
            )
            .order_by("-id")
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        comment = self.get_object()
        Like.objects.get_or_create(user=request.user, comment=comment, defaults={"post": None})
        return Response({"status": "liked"}, status=status.HTTP_200_OK)

    @like.mapping.delete
    def unlike(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        comment = self.get_object()
        Like.objects.filter(user=request.user, comment=comment).delete()
        return Response({"status": "unliked"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def by_post(self, request):
        """
        Lightweight comments for a post.
        GET /api/comments/by_post/?post_id=2
        """
        post_id = request.query_params.get("post_id")
        if not post_id:
            return Response({"detail": "post_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        qs = (
            Comment.objects.filter(post_id=post_id)
            .annotate(
                likes_count=Count("like", filter=Q(like__comment__isnull=False), distinct=True)
            )
            .order_by("-id")
        )
        data = [
            {"id": c.id, "content": c.content, "author": c.author_id, "likes_count": c.likes_count}
            for c in qs
        ]
        return Response(data, status=status.HTTP_200_OK)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all().order_by("-id")
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

