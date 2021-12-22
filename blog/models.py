from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} liked {self.post}"
