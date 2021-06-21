from django.urls import path
from . import views


app_name = 'profile'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('change-password/', views.change_pass, name='change_pass'),
    path('update-user-info/', views.update_profile, name='update_user'),
    path('<pk>/', views.OtherUserProfile.as_view(), name='user_profile'),
    path('change-profile-picture/<pk>/', views.UpdatePfp.as_view(), name='update_pfp'),
    path('follow/<int:pk>/', views.follow, name='follow'),
    path('unfollow/<int:pk>/', views.unfollow, name='unfollow'),
    path('check-notification/<int:pk>/', views.check_notification, name='check_notification'),
    path('followers/<int:pk>/', views.follower_list, name='followers'),
    path('following/<int:pk>/', views.following_list, name='following'),
    path('post-likes/<int:pk>/', views.post_likers, name='post_likers'),
    path('comment-likes/<int:pk>/', views.comment_likers, name='comment_likers'),
]