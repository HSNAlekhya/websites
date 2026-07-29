from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Friend

@receiver(post_save, sender=User)
def create_friend(sender, instance, created, **kwargs):
    if created:
        Friend.objects.create(user=instance)