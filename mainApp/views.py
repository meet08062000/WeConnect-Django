from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Like, Follow
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    following = Follow.objects.filter(follower_id=request.user.id).all()
    following_id = [x.receiver_id for x in following]
    following_id += [request.user.id]
    posts = []
    likes = list(Like.objects.filter(user_id=request.user.id))
    liked_post_ids = [x.post_id for x in likes]
    for x in following_id:
        posts += Post.objects.filter(author_id=x)
    context = {
        'posts': sorted(posts, key=lambda x: x.timestamp, reverse=True),
        'user_id': request.user.id,
        'liked_post_ids': liked_post_ids,
        'title': 'Dashboard'
    }
    return render(request, 'mainApp/dashboard.html', context)


@login_required
def createpost(request):
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
        #post.title = ''
        #post.desc = ''
        #post.image = ''
        #post.loc = ''
        #post.tags = ''
        #post.author_id = ''
        # , {'post': post, 'title': 'Create Post'}
        return render(request, 'mainApp/createpost.html', {'user_id': request.user.id})


@login_required
def like(request, post_id):
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


@login_required
def profile(request, user_id):
    user = User.objects.filter(id=user_id).get()
    posts = Post.objects.filter(author=user)
    posts_count = Post.objects.filter(author=user).count()
    likes = list(Like.objects.filter(user_id=request.user.id))
    liked_post_ids = [x.post_id for x in likes]
    if(Follow.objects.filter(follower_id=request.user.id, receiver_id=user_id).count() != 0):
        follows = True
    else:
        follows = False
    context = {
        'user': user,
        'current_user_id': request.user.id,
        'posts': sorted(posts, key=lambda x: x.timestamp, reverse=True),
        'posts_count': posts,
        'posts_count': posts_count,
        'follows': follows,
        'liked_post_ids': liked_post_ids,
        'title': 'User profile',
        'user_id': request.user.id,
    }
    return render(request, 'mainApp/profile.html', context)


@login_required
def follows(request, user_id):
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


@login_required
def editpost(request, post_id):
    if (request.method.lower() == 'post'):
        post_list = Post.objects.filter(id=post_id)
        post = post_list[0]
        post.title = request.POST['title']
        post.desc = request.POST['desc']
        if(request.FILES):
            post.image = request.FILES['image']
        post.loc = request.POST['loc']
        post.tags = request.POST['tags']
        post.save()
        return redirect('/app')
    else:
        post_list = Post.objects.filter(id=post_id)
        post = post_list[0]
        if(post.author_id == request.user.id):
            return render(request, 'mainApp/editpost.html', {'post': post, 'title': 'Edit post', 'user_id': request.user.id})
        else:
            return redirect('/app')


@login_required
def editprofile(request):
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
        return render(request, 'mainApp/editprofile.html', {'user': user, 'title': 'Edit profile', 'user_id': request.user.id})


def post_delete(request, post_id):
    post = Post.objects.filter(id=post_id)
    post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
