from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    media = models.FileField(upload_to='post_media/', null=True)
    loc = models.CharField(max_length=100, default='', null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=10, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_or_not = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     super(Post, self).save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        path = ''
        if self.media:
            storage, path = self.media.storage, self.media.path
        # Delete the model before the file
        super(Post, self).delete(*args, **kwargs)
        # Delete the file after the model
        if path:
            storage.delete(path)


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follow')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')


class Bookmark(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookmark')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='bookmark')


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comment')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.message


class Reply(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reply')
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.message


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='like')
    post = models.ForeignKey(
        Post, null=True, on_delete=models.CASCADE, related_name='like')
    comment = models.ForeignKey(
        Comment, null=True, on_delete=models.CASCADE, related_name='like')
    reply = models.ForeignKey(
        Reply, null=True, on_delete=models.CASCADE, related_name='like')
