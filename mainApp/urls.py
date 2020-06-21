from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('post', views.createpost, name="createpost"),
    path('profile/<int:user_id>', views.profile, name="profile"),
    path('search', views.search, name='search'),
    path('follow/<int:user_id>', views.follow, name="follow"),
    path('<int:post_id>', views.like, name="like"),
    path('post/<int:post_id>', views.editpost,
         name="editpost"),
    path('post_delete/<int:post_id>', views.post_delete,
         name="post_delete"),
    path('editprofile', views.editprofile, name="editprofile"),
    path('bookmark/<int:post_id>', views.bookmark, name='bookmark')
]
