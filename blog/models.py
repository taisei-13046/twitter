from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']


class Follow(models.Model):
    follow_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follow_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.follow_from} follows {self.follow_to}"

    class Meta:
        db_table = 'follow'
