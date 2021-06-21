from django.urls import path
from .views import CreatePost, DeletePost, EditComment, EditPost, ViewPost, comment_like, comment_unlike, delete_comment, feed, post_like, post_unlike, share, share_list, write_comment


app_name = 'post'

urlpatterns = [
    path('', feed, name='feed'),
    path('post/', CreatePost.as_view(), name='create_post'),
    path('post/<pk>/', ViewPost.as_view(), name='single_post'),
    path('edit-post/<pk>/', EditPost.as_view(), name='edit_post'),
    path('delete-post/<pk>/', DeletePost.as_view(), name='delete_post'),
    path('like-post/<int:pk>/', post_like, name='post_like'),
    path('unlike-post/<int:pk>/', post_unlike, name='post_unlike'),
    path('comment/<int:pk>/', write_comment, name='comment'),
    path('edit-comment/<int:pk>/', EditComment.as_view(), name='edit_comment'),
    path('delete-comment/<int:pk>/', delete_comment, name='delete_comment'),
    path('like-comment/<int:pk>/', comment_like, name='comment_like'),
    path('unlike-comment/<int:pk>/', comment_unlike, name='comment_unlike'),
    path('share-post/<pk>/', share_list, name='share_list'),
    path('share/<pk>/', share, name='share'),
]