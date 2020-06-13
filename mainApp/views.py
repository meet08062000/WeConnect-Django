from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.


def dashboard(request):
    print(request.user)
    if(request.user.is_authenticated):
        posts = Post.objects.all()
        return render(request, 'dashboard.html', {'posts': sorted(posts, key=lambda x: x.timestamp, reverse=True)})
    else:
        return redirect('/')


def post(request):
    if (request.method == 'POST'):
        post = Post()
        post.title = request.POST['title']
        post.desc = request.POST['desc']
        post.image = request.FILES['image']
        post.loc = request.POST['loc']
        post.tags = request.POST['tags']
        post.author_id = request.user.id
        post.save()
        redirect('/dashboard')
    else:
        return render(request, 'post.html')
