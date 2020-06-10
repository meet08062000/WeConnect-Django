from django.shortcuts import render
from .models import Post

# Create your views here.
def dashboard (request):
    posts = Post.objects.all()
    
    return render (request, 'dashboard.html',{'posts':posts})