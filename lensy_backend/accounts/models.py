from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.conf import settings
import os

User = settings.AUTH_USER_MODEL


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('user', 'user'),
        ('admin', 'admin')
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()



class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'following')

    
@receiver(pre_save, sender=CustomUser)
def delete_old_avatar_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_avatar = CustomUser.objects.get(pk=instance.pk).avatar
    except CustomUser.DoesNotExist:
        return

    new_avatar = instance.avatar

    if old_avatar and old_avatar != new_avatar:
        if old_avatar.storage.exists(old_avatar.name):
            old_avatar.storage.delete(old_avatar.name)


@receiver(post_delete, sender=CustomUser)
def delete_avatar_on_user_delete(sender, instance, **kwargs):
    if instance.avatar:
        if instance.avatar.storage.exists(instance.avatar.name):
            instance.avatar.storage.delete(instance.avatar.name)