from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Like, Follow
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.db.models.query_utils import Q
from mainApp.models import Bookmark, Comment, Reply
from django.http import JsonResponse
from django.template.loader import render_to_string


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
        if(request.FILES):
            post.media = request.FILES['media']
        if(request.POST['loc']):
            post.loc = request.POST['loc']
        if(request.POST['tags']):
            post.tags = request.POST['tags']
        post.author_id = request.user.id
        post.save()
        return redirect('/app')
    else:
        post = Post()
        post.title = ''
        post.desc = ''
        post.media = ''
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
def like(request):
    if(request.method.lower() == 'post'):
        post_id = request.POST['post_id']
        like_count = Like.objects.filter(
            user_id=request.user.id, post_id=post_id).count()
        post = Post.objects.filter(id=post_id).get()
        if(like_count != 0):
            post.likes -= 1
            post.save()
            like = Like.objects.filter(
                user_id=request.user.id, post_id=post_id).get()
            like.delete()
            context = {
                'post': post,
            }
        else:
            like = Like()
            like.user_id = request.user.id
            like.post_id = post_id
            post.likes += 1
            post.save()
            like.save()
            context = {
                'post': post,
            }
        if request.is_ajax():
            html = render_to_string(
                'mainApp/like_section.html', context, request=request)
            return JsonResponse({'form': html})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def like_comment(request):
    if(request.method.lower() == 'post'):
        comment_id = request.POST['comment_id']
        like_count = Like.objects.filter(
            user_id=request.user.id, comment_id=comment_id).count()
        comment = Comment.objects.filter(id=comment_id).get()
        if(like_count != 0):
            comment.likes -= 1
            comment.save()
            like = Like.objects.filter(
                user_id=request.user.id, comment_id=comment_id).get()
            like.delete()
            context = {
                'comment': comment,
            }
        else:
            like = Like()
            like.user_id = request.user.id
            like.comment_id = comment_id
            comment.likes += 1
            comment.save()
            like.save()
            context = {
                'comment': comment,
            }
        if request.is_ajax():
            html = render_to_string(
                'mainApp/like_comment_section.html', context, request=request)
            return JsonResponse({'form': html})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def like_reply(request):
    if(request.method.lower() == 'post'):
        reply_id = request.POST['reply_id']
        like_count = Like.objects.filter(
            user_id=request.user.id, reply_id=reply_id).count()
        reply = Reply.objects.filter(id=reply_id).get()
        if(like_count != 0):
            reply.likes -= 1
            reply.save()
            like = Like.objects.filter(
                user_id=request.user.id, reply_id=reply_id).get()
            like.delete()
            context = {
                'reply': reply,
            }
        else:
            like = Like()
            like.user_id = request.user.id
            like.reply_id = reply_id
            reply.likes += 1
            reply.save()
            like.save()
            context = {
                'reply': reply,
            }
        if request.is_ajax():
            html = render_to_string(
                'mainApp/like_reply_section.html', context, request=request)
            return JsonResponse({'form': html})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def profile(request, user_id):
    profile = User.objects.filter(id=user_id).get()
    posts = Post.objects.all()
    posts_count = profile.post_set.count()
    likes = list(request.user.like.all())
    bookmark = list(request.user.bookmark.all())
    bookmark_ids = [x.post_id for x in bookmark]
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
        'following_list': request.user.follow.all(),
        'bookmarks': bookmark_ids
    }
    return render(request, 'mainApp/profile.html', context)


@login_required
def follow(request):
    if(request.method.lower() == "post"):
        user_id = request.POST['user_id']
        user = User.objects.filter(id=user_id)
        follow_count = Follow.objects.filter(
            follower=request.user.id, receiver=user_id).count()
        if (follow_count != 0):
            follow = request.user.follow.filter(receiver_id=user_id).delete()
            context = {
                'profile': user,
                'follows': False
            }
        else:
            follow = Follow()
            follow.follower_id = request.user.id
            follow.receiver_id = user_id
            follow.save()
            context = {
                'profile': user,
                'follows': True
            }
        if request.is_ajax():
            html = render_to_string(
                'mainApp/follow_section.html', context, request=request)
            return JsonResponse({'form': html})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def editpost(request, post_id):
    if (request.method.lower() == 'post'):
        post_list = Post.objects.filter(id=post_id)
        post = post_list[0]
        post.title = request.POST['title']
        post.desc = request.POST['desc']
        if(request.FILES):
            post.media = request.FILES['media']
        if(request.POST['loc']):
            post.loc = request.POST['loc']
        if(request.POST['tags']):
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
        return redirect('profile', request.user.id)
    else:
        user = request.user
        return render(request, 'mainApp/editprofile.html', {'title': 'Edit profile', 'following_list': request.user.follow.all()})


@login_required
def post_delete(request, post_id):
    post = Post.objects.filter(id=post_id).get()
    # if(post.media):
    #     post.media.delete()
    if(post.author == request.user):
        post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def search(request):
    search = request.GET['search']
    results = User.objects.filter(Q(first_name__contains=search) | Q(
        username__contains=search) | Q(last_name__contains=search) | Q(email__contains=search))
    follow_list = []
    i = 0
    for user in results:
        user_id = user.id
        if(request.user.follow.filter(receiver_id=user_id).count() != 0):
            follow_list.append(user_id)
        i += 1
    context = {
        'results': results,
        'following_list': request.user.follow.all(),
        'follow_list': follow_list
    }
    if results is not None:
        return render(request, 'mainApp/search.html', context)
    else:
        messages.info(request, 'No results found!')
        return redirect('dashboard')


@login_required
def bookmark(request):
    if(request.method.lower() == 'post'):
        post_id = request.POST['post_id']
        bookmark_count = Bookmark.objects.filter(
            user_id=request.user.id, post_id=post_id).count()
        post = Post.objects.filter(id=post_id).get()
        if(bookmark_count != 0):
            bookmark = Bookmark.objects.filter(
                user_id=request.user.id, post_id=post_id).get()
            bookmark.delete()
            context = {
                'post': post
            }
        else:
            bookmark = Bookmark()
            bookmark.user_id = request.user.id
            bookmark.post_id = post_id
            bookmark.save()
            context = {
                'post': post
            }
        if request.is_ajax():
            html = render_to_string(
                'mainApp/bookmark_section.html', context, request=request)
            return JsonResponse({'form': html})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def comment(request, post_id):
    if request.method.lower() == 'post':
        message = request.POST['message']
        post = Post.objects.filter(id=post_id).get()
        comment = Comment()
        comment.message = message
        comment.user = request.user
        comment.post = post
        comment.save()
        return redirect('post_page', post_id)
    return redirect('post_page', post_id)


@login_required
def reply(request, post_id, comment_id):
    if request.method.lower() == 'post':
        message = request.POST['message']
        comment = Comment.objects.filter(id=comment_id).get()
        reply = Reply()
        reply.message = message
        reply.user = request.user
        reply.comment = comment
        reply.save()
        return redirect('post_page', post_id)
    return redirect('post_page', post_id)


@login_required
def post_page(request, post_id):
    post = Post.objects.filter(id=post_id).get()
    liked_posts = list(request.user.like.all())
    liked_post_ids = [x.post_id for x in liked_posts]
    liked_comments = list(request.user.like.all())
    liked_comment_ids = [x.comment_id for x in liked_comments]
    liked_replies = list(request.user.like.all())
    liked_reply_ids = [x.reply_id for x in liked_replies]
    bookmark = list(request.user.bookmark.all())
    bookmark_ids = [x.post_id for x in bookmark]
    comments = post.comment.all()
    context = {
        'post': post,
        'liked_post_ids': liked_post_ids,
        'liked_comment_ids': liked_comment_ids,
        'liked_reply_ids': liked_reply_ids,
        'bookmarks': bookmark_ids,
        'comments': sorted(comments, key=lambda x: x.timestamp, reverse=True)
    }
    return render(request, 'mainApp/post_page.html', context)


@login_required
def comment_delete(request, comment_id):
    comment = Comment.objects.filter(id=comment_id).get()
    if request.user == comment.user:
        comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def reply_delete(request, reply_id):
    reply = Reply.objects.filter(id=reply_id).get()
    if request.user == reply.user:
        reply.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
