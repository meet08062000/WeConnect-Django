from django.contrib import admin
from .models import Post, Like, Follow, Bookmark, Comment, Reply

# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Bookmark)
admin.site.register(Comment)
admin.site.register(Reply)
