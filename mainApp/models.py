from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    image = models.ImageField(upload_to='post_images')
    loc = models.CharField(max_length=100, default='')
    timestamp = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=10)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_or_not = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='like')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post')


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follow')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')
