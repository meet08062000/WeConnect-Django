from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Like, Follow
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.db.models.query_utils import Q
from mainApp.models import Bookmark


@login_required
def dashboard(request):
    following = Follow.objects.filter(follower_id=request.user.id).all()
    following_id = [x.receiver_id for x in following]
    following_id += [request.user.id]
    posts = []
    likes = list(request.user.like.all())
    liked_post_ids = [x.post_id for x in likes]
    bookmarks = list(request.user.bookmark.all())
    bookmarks_post_id = [x.post_id for x in bookmarks]
    for x in following_id:
        posts += Post.objects.filter(author_id=x)
    context = {
        'posts': sorted(posts, key=lambda x: x.timestamp, reverse=True),
        'liked_post_ids': liked_post_ids,
        'bookmarks': bookmarks_post_id,
        'title': 'Dashboard',
        'following_list': request.user.follow.all()
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
        post.title = ''
        post.desc = ''
        post.image = ''
        post.loc = ''
        post.tags = ''
        post.author_id = ''
        context = {
            'post': post,
            'title': 'Create Post',
            'following_list': request.user.follow.all()
        }
        return render(request, 'mainApp/createpost.html', context)


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
    profile = User.objects.filter(id=user_id).get()
    posts = profile.post_set.all()
    posts_count = posts.count()
    likes = list(request.user.like.all())
    liked_post_ids = [x.post_id for x in likes]
    following_count = Follow.objects.filter(follower_id=profile.id).count()
    follower_count = Follow.objects.filter(receiver_id=profile.id).count()
    if(request.user.follow.filter(receiver_id=user_id).count() != 0):
        follows = True
    else:
        follows = False
    context = {
        'profile': profile,
        'posts': sorted(posts, key=lambda x: x.timestamp, reverse=True),
        'posts_count': posts_count,
        'follower_count': follower_count,
        'following_count': following_count,
        'follows': follows,
        'liked_post_ids': liked_post_ids,
        'title': 'User profile',
        'following_list': request.user.follow.all()
    }
    return render(request, 'mainApp/profile.html', context)


@login_required
def follow(request, user_id):
    if(request.method.lower() == "post"):
        follow_count = Follow.objects.filter(
            follower=request.user.id, receiver=user_id).count()
        if (follow_count != 0):
            follow = request.user.follow.filter(receiver_id=user_id).delete()
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
            return render(request, 'mainApp/editpost.html', {'post': post, 'title': 'Edit post', 'following_list': request.user.follow.all()})
        else:
            return redirect('/app')


@login_required
def editprofile(request):
    if (request.method.lower() == 'post'):
        user = request.user
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        if request.FILES:
            user.profile.image = request.FILES['image']
        # user.dob = request.POST['dob']
        user.email = request.POST['email']
        user.profile.desc = request.POST['desc']
        user.save()
        return redirect('/app')
    else:
        user = request.user
        return render(request, 'mainApp/editprofile.html', {'title': 'Edit profile', 'following_list': request.user.follow.all()})


def post_delete(request, post_id):
    post = Post.objects.filter(id=post_id).get()
    # if(post.image):
    #     post.image.delete()
    post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def search(request):
    search = request.GET['search']
    results = User.objects.filter(Q(first_name__contains=search) | Q(
        username__contains=search) | Q(last_name__contains=search) | Q(email__contains=search))
    if results is not None:
        return render(request, 'mainApp/search.html', {'results': results, 'following_list': request.user.follow.all()})
    else:
        messages.info(request, 'No results found!')
        return redirect('dashboard')


@login_required
def bookmark(request, post_id):
    bookmark_count = Bookmark.objects.filter(
        user_id=request.user.id, post_id=post_id).count()
    if(bookmark_count != 0):
        bookmark = Bookmark.objects.filter(
            user_id=request.user.id, post_id=post_id).get()
        bookmark.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        bookmark = Bookmark()
        bookmark.user_id = request.user.id
        bookmark.post_id = post_id
        bookmark.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
