from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Follow(models.Model):
    follow_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follow_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.follow_from} follows {self.follow_to}"

    class Meta:
        db_table = 'follow'
