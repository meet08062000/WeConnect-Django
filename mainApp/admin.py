from django.contrib import admin
from .models import Post, Likes, Follows

# Register your models here.
admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(Follows)