from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name="friend_list")

    def __str__(self):
        return self.user.username


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name="sent_requests",
        on_delete=models.CASCADE
    )

    to_user = models.ForeignKey(
        User,
        related_name="received_requests",
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"{self.from_user} → {self.to_user}"

# Create your models here.
