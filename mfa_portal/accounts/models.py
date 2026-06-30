from django.db import models
from django.contrib.auth.models import User

class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)

    def __str__(self):
        return self.user.username

# Create your models here.
