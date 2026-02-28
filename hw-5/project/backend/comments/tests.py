from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Post, Comment, Like


class TestLikeComment(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="dima",
            email="dima@test.com",
            password="123456",
        )

        self.post = Post.objects.create(
            title="First post",
            content="Hello world",
            author=self.user,
        )

        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="My first comment",
        )

    def test_like_comment(self) -> None:
        self.client.force_authenticate(user=self.user)

        resp = self.client.post(f"/api/comments/{self.comment.id}/like/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], "liked")

        self.assertTrue(
            Like.objects.filter(user=self.user, comment=self.comment).exists()
        )

    def test_unlike_comment(self) -> None:
        self.client.force_authenticate(user=self.user)

        self.client.post(f"/api/comments/{self.comment.id}/like/")

        resp = self.client.delete(f"/api/comments/{self.comment.id}/like/")
        self.assertIn(resp.status_code, (200, 204))

        self.assertFalse(
            Like.objects.filter(user=self.user, comment=self.comment).exists()
        )
