from django.conf import settings
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Owner: {self.user.email} Content {self.content}"


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_likes"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Owner: {self.user.email} Content {self.content}"


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follower"
    )
    followed = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"follower: {self.follower.email}  followed {self.followed.email}"
