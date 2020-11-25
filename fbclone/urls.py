from django.contrib import admin
from django.urls import path,include
from fbclone import views

urlpatterns = [
    path('',views.home, name="home"),
    path('login', views.login_user, name="login_user"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name="logout"),
    path('search', views.search, name="search"),
    path('profile', views.profile, name='profile'),
    path('profile_update/<int:id>', views.profile_update, name='profile_update'),
    #path('afterSearch/<int:id>', views.afterSearch, name="afterSearch"),
    path('cover_update/<int:id>', views.update_cover, name="update_cover"),
    path('delete/<int:id>', views.delete_post, name="delete_post"),
    # path('second_home', views.second_home, name="second_home"),
    path('add_friend/<int:id>', views.add_friend, name="add_friend"),
    path('accept_friend/<int:id>', views.accept_friend, name="accept_friend"),
    path('afterSearch/<int:id>', views.blogPost, name="afterSearch"),
    path('postComment', views.postComment, name="postComment"),
    path('comment/<int:sno>', views.comment, name="comment"),
    path('friendRequest', views.friendRequest, name="friendRequest"),
    path('remove_friend/<int:id>', views.Remove_friend, name="remove_friend"),
    path('chat/<int:id>', views.chat, name="chat"),
    path('chatMessage/<int:id>', views.message_system, name="chatMessage"),
    path('messagedelete/<int:id>', views.messageDelete, name="messagedelete"),
    path('notification', views.notification, name="notification"),
    path('likes/<int:sno>/<int:id>', views.likes, name="likes"),
    path('self_like/<int:sno>', views.self_like, name="self_like"),
    path('common_like/<int:sno>', views.common_like, name="common_like"),
]
