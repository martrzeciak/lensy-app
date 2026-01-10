from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Hashtag

@receiver(post_save, sender=Post)
def save_hashtags(sender, instance, **kwargs):
    instance.hashtags.clear()
    tags = instance.extract_hashtags()

    for tag in tags:
        hashtag, _ = Hashtag.objects.get_or_create(name=tag.lower())
        instance.hashtags.add(hashtag)
