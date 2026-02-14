from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Post(id={self.id}, title={self.title})"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Comment(id={self.id}, post_id={self.post_id})"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    (Q(post__isnull=False) & Q(comment__isnull=True)) |
                    (Q(post__isnull=True) & Q(comment__isnull=False))
                ),
                name="like_exactly_one_target",
            ),
            models.UniqueConstraint(fields=["user", "post"], name="uniq_user_post_like"),
            models.UniqueConstraint(fields=["user", "comment"], name="uniq_user_comment_like"),
        ]

    def __str__(self) -> str:
        target = f"post_id={self.post_id}" if self.post_id is not None else f"comment_id={self.comment_id}"
        return f"Like(id={self.id}, user_id={self.user_id}, {target})"
