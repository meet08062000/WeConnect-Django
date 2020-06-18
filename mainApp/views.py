from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Like, Follow
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.


def dashboard(request):
    if(request.user.is_authenticated):
        following = Follow.objects.filter(follower_id=request.user.id).all()
        following_id = [x.receiver_id for x in following]
        following_id += [request.user.id]
        posts = []
        likes = list(Like.objects.filter(user_id=request.user.id))
        liked_post_ids = [x.post_id for x in likes]
        for x in following_id:
            posts += Post.objects.filter(author_id=x)
        return render(request, 'mainApp/dashboard.html', {'posts': sorted(posts, key=lambda x: x.timestamp, reverse=True), 'user_id': request.user.id, 'liked_post_ids': liked_post_ids})
    else:
        return redirect('/')


def createpost(request):
    if(request.user.is_authenticated):
        if (request.method == 'POST'):
            post = Post()
            post.title = request.POST['title']
            post.desc = request.POST['desc']
            post.image = request.FILES['image']
            post.loc = request.POST['loc']
            post.tags = request.POST['tags']
            post.author_id = request.user.id
            post.save()
            return redirect('/app')
        else:
            post = Post()
            post.title = ''
            post.desc = ''
            post.image = ''
            post.loc = ''
            post.tags = ''
            post.author_id = ''
            return render(request, 'mainApp/createpost.html', {'post': post})
    else:
        return redirect('/')


def userprofile(request):
    if(request.user.is_authenticated):
        if (request.method.lower() == 'post'):
            pass
        else:
            logged_in_user_posts = Post.objects.filter(author=request.user)
            posts_count = logged_in_user_posts.count()
            likes = list(Like.objects.filter(user_id=request.user.id))
            liked_post_ids = [x.post_id for x in likes]
            return render(request, 'mainApp/userprofile.html', {'profile': request.user, 'userposts': logged_in_user_posts, 'posts_count': posts_count, 'liked_post_ids': liked_post_ids})
    else:
        return redirect('/')


def like(request, post_id):
    if(request.user.is_authenticated):
        like_count = Like.objects.filter(
            user_id=request.user.id, post_id=post_id).count()
        post = Post.objects.filter(id=post_id).get()
        if(like_count != 0):
            post.likes -= 1
            post.save()
            like = Like.objects.filter(
                user_id=request.user.id, post_id=post_id).get()
            like.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            like = Like()
            like.user_id = request.user.id
            like.post_id = post_id
            post.likes += 1
            post.save()
            like.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/')


def profile(request, user_id):
    if(request.user.is_authenticated):
        if(user_id != request.user.id):
            user = User.objects.filter(id=user_id).get()
            user_posts = Post.objects.filter(author=user)
            user_posts_count = Post.objects.filter(author=user).count()
            likes = list(Like.objects.filter(user_id=request.user.id))
            liked_post_ids = [x.post_id for x in likes]
            if(Follow.objects.filter(follower_id=request.user.id, receiver_id=user_id).count() != 0):
                follows = True
            else:
                follows = False
            return render(request, 'mainApp/profile.html', {'user': user, 'userposts': user_posts, 'posts_count': user_posts, 'posts_count': user_posts_count, 'follows': follows, 'liked_post_ids': liked_post_ids})
        else:
            return redirect('/app/userprofile')
    else:
        return redirect('/')


def follows(request, user_id):
    if(request.user.is_authenticated):
        if(request.method.lower() == "post"):
            follow_count = Follow.objects.filter(
                follower=request.user.id, receiver=user_id).count()
            if (follow_count != 0):
                follow = Follow.objects.filter(receiver=user_id).delete()
                return redirect('/app/profile/{}'.format(user_id))
            else:
                follow = Follow()
                follow.follower_id = request.user.id
                follow.receiver_id = user_id
                follow.save()
                return redirect('/app/profile/{}'.format(user_id))
    else:
        return redirect('/')


def editpost(request, post_id):
    if(request.user.is_authenticated):
        if (request.method.lower() == 'post'):
            post_list = Post.objects.filter(id=post_id)
            post = post_list[0]
            post.title = request.POST['title']
            post.desc = request.POST['desc']
            post.image = request.FILES['image']
            post.loc = request.POST['loc']
            post.tags = request.POST['tags']
            post.save()
            return redirect('/app')
        else:
            post_list = Post.objects.filter(id=post_id)
            post = post_list[0]
            if(post.author_id == request.user.id):
                return render(request, 'mainApp/editpost.html', {'post': post})
            else:
                return redirect('/app')
    else:
        return redirect('/')


def editprofile(request):
    if(request.user.is_authenticated):
        if (request.method.lower() == 'post'):
            user = request.user
            user.username = request.POST['username']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            # user.image = request.FILES['image']
            # user.dob = request.POST['dob']
            user.email = request.POST['email']
            user.save()
            return redirect('/app')
        else:
            user = request.user
            return render(request, 'mainApp/editprofile.html', {'user': user})
    else:
        return redirect('/')
