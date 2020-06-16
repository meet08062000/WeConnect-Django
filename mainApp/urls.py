from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('post', views.post, name="post"),
    path('profilepage', views.profilepage, name="profilepage"),
    path('profile/<int:user_id>', views.profile, name="profile"),
    path('<int:post_id>', views.like, name="like")
]
