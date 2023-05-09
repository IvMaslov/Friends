from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Friends(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_id")
    friend_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_id")
    time = models.TimeField()
    status = models.CharField(max_length=10)

    class Meta:
        unique_together = (("user_id", "friend_id"), )

class FriendRequest(models.Model):
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender_id")
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver_id")
    status = models.CharField(max_length=10)

    class Meta:
        unique_together = (("sender_id", "receiver_id"), )