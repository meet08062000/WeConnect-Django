from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('post', views.post, name="post"),
    path('userprofile', views.userprofile, name="userprofile"),
    path('profile/<int:user_id>', views.profile, name="profile"),
    path('follows/<int:user_id>', views.follows, name="follows"),
    path('<int:post_id>', views.like, name="like")
]
