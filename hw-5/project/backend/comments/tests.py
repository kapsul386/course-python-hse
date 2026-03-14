from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Post, Comment, Like


class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.u1 = User.objects.create_user(username="u1", password="pass12345")
        self.u2 = User.objects.create_user(username="u2", password="pass12345")

        self.post = Post.objects.create(title="t", content="c", author=self.u1)
        self.comment = Comment.objects.create(post=self.post, content="x", author=self.u1)

    # --- Public read access ---
    def test_posts_list_public(self):
        resp = self.client.get("/api/posts/")
        self.assertEqual(resp.status_code, 200)

    def test_comments_list_public(self):
        resp = self.client.get("/api/comments/")
        self.assertEqual(resp.status_code, 200)

    # --- Create requires auth (IsAuthenticatedOrReadOnly) ---
    def test_posts_create_requires_auth_and_ignores_author_spoof(self):
        resp = self.client.post(
            "/api/posts/",
            {"title": "a", "content": "b", "author": self.u2.id},
            format="json",
        )
        self.assertIn(resp.status_code, (401, 403))

        self.client.login(username="u1", password="pass12345")
        resp = self.client.post(
            "/api/posts/",
            {"title": "a", "content": "b", "author": self.u2.id},
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data["author"], self.u1.id)

    def test_comments_create_requires_auth_and_ignores_author_spoof(self):
        resp = self.client.post(
            "/api/comments/",
            {"post": self.post.id, "author": self.u2.id, "content": "hello"},
            format="json",
        )
        self.assertIn(resp.status_code, (401, 403))

        self.client.login(username="u1", password="pass12345")
        resp = self.client.post(
            "/api/comments/",
            {"post": self.post.id, "author": self.u2.id, "content": "hello"},
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data["author"], self.u1.id)

    # --- User permissions ---
    def test_user_update_only_self_or_admin(self):
        self.client.login(username="u2", password="pass12345")
        resp = self.client.patch(f"/api/users/{self.u1.id}/", {"first_name": "hack"}, format="json")
        self.assertIn(resp.status_code, (401, 403))

        self.client.logout()
        self.client.login(username="u1", password="pass12345")
        resp = self.client.patch(f"/api/users/{self.u1.id}/", {"first_name": "ok"}, format="json")
        self.assertEqual(resp.status_code, 200)

    # --- Author permissions (IsAuthorOrReadOnly) ---
    def test_post_update_only_author(self):
        self.client.login(username="u2", password="pass12345")
        resp = self.client.patch(f"/api/posts/{self.post.id}/", {"title": "hacked"}, format="json")
        self.assertIn(resp.status_code, (401, 403))

        self.client.logout()
        self.client.login(username="u1", password="pass12345")
        resp = self.client.patch(f"/api/posts/{self.post.id}/", {"title": "ok"}, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_comment_delete_only_author(self):
        self.client.login(username="u2", password="pass12345")
        resp = self.client.delete(f"/api/comments/{self.comment.id}/")
        self.assertIn(resp.status_code, (401, 403))

        self.client.logout()
        self.client.login(username="u1", password="pass12345")
        resp = self.client.delete(f"/api/comments/{self.comment.id}/")
        self.assertIn(resp.status_code, (200, 204))

    # --- Likes require auth ---
    def test_like_unlike_post_requires_auth(self):
        resp = self.client.post(f"/api/posts/{self.post.id}/like/")
        self.assertIn(resp.status_code, (401, 403))

        self.client.login(username="u1", password="pass12345")
        resp = self.client.post(f"/api/posts/{self.post.id}/like/")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.delete(f"/api/posts/{self.post.id}/like/")
        self.assertEqual(resp.status_code, 200)

    def test_like_unlike_comment_requires_auth(self):
        resp = self.client.post(f"/api/comments/{self.comment.id}/like/")
        self.assertIn(resp.status_code, (401, 403))

        self.client.login(username="u1", password="pass12345")
        resp = self.client.post(f"/api/comments/{self.comment.id}/like/")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.delete(f"/api/comments/{self.comment.id}/like/")
        self.assertEqual(resp.status_code, 200)

    def test_like_create_ignores_user_spoof(self):
        self.client.login(username="u1", password="pass12345")
        resp = self.client.post(
            "/api/likes/",
            {"user": self.u2.id, "post": self.post.id, "comment": None},
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        like = Like.objects.get(id=resp.data["id"])
        self.assertEqual(like.user_id, self.u1.id)

    # --- Aggregated endpoints ---
    def test_posts_top(self):
        resp = self.client.get("/api/posts/top/")
        self.assertEqual(resp.status_code, 200)

    def test_comments_by_post(self):
        resp = self.client.get(f"/api/comments/by_post/?post_id={self.post.id}")
        self.assertEqual(resp.status_code, 200)

    def test_comments_by_post_requires_param(self):
        resp = self.client.get("/api/comments/by_post/")
        self.assertEqual(resp.status_code, 400)
