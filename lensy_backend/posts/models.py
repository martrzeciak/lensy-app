from django.db import models
from django.conf import settings
from django.urls import reverse
import re

User = settings.AUTH_USER_MODEL



class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"#{self.name}"


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    image = models.ImageField(upload_to='posts/')
    description = models.TextField(blank=True)
    hashtags = models.ManyToManyField(
        Hashtag,
        blank=True,
        related_name='posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post {self.id} by {self.author}"

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id])

    def extract_hashtags(self):
        tags = set(re.findall(r"#(\w+)", self.description))
        return tags


class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user}"
    

class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'comment')