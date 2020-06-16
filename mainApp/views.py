from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Likes, Follows
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
        return redirect('/app')
    else:
        return render(request, 'post.html')


def userprofile(request):
    if (request.method.lower() == 'post'):
        pass
    else:
        logged_in_user_posts = Post.objects.filter(author=request.user)
        posts_count = logged_in_user_posts.count()
        return render(request, 'userprofile.html', {'userposts': logged_in_user_posts, 'posts_count': posts_count})


def like(request, post_id):
    if(request.method.lower() == "post"):
        like_count = Likes.objects.filter(
            user_id=request.user.id, post_id=post_id).count()
        post = Post.objects.filter(id=post_id).get()
        if(like_count != 0):
            post.likes -= 1
            post.save()
            like = Likes.objects.filter(
                user_id=request.user.id, post_id=post_id).get()
            like.delete()
        else:
            like = Likes()
            like.user_id = request.user.id
            like.post_id = post_id
            post.likes += 1
            post.save()
            like.save()
        return redirect('/app')


def profile(request, user_id):
    if(user_id != request.user.id):
        user = User.objects.filter(id=user_id).get()
        user_posts = Post.objects.filter(author=user)
        user_posts_count = Post.objects.filter(author=user).count()
        return render(request, 'profile.html', {'user': user, 'userposts': user_posts, 'posts_count': user_posts, 'posts_count': user_posts_count})
    else:
        return redirect('/app/userprofile')


def follows(request, user_id):
    if(request.method.lower() == "post"):
        follow_count = Follows.objects.filter(
            follower=request.user.id, receiver=user_id).count()
        if (follow_count != 0):
            follow = Follows.objects.filter(receiver=user_id).delete()
            return redirect('/app/profile/{}'.format(user_id))
        else:
            follow = Follows()
            follow.follower_id = request.user.id
            follow.receiver_id = user_id
            follow.save()
            return redirect('/app/profile/{}'.format(user_id))
