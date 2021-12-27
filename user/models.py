from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.following} follows {self.follower}"

    class Meta:
        db_table = 'follow'
