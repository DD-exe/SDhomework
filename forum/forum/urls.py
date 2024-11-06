# urls.py

from django.conf import settings
from django.conf.urls import include
from django.urls import path
from .views import home, post_list, new_post, delete_post, edit_post, post_detail, collect_post, remove_collect, collected_posts, new_comment, delete_comment, new_reply, delete_reply

urlpatterns = [

    path('home/', home, name='home'),
    path('PostList/', post_list, name='post_list'),
    path('NewPost/', new_post, name='new_post'),
    path('delete/<int:post_id>/', delete_post, name='delete_post'),
    path('EditPost/<int:post_id>/', edit_post, name='edit_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/collect/', collect_post, name='collect_post'),
    path('post/<int:post_id>/remove-collect/', remove_collect, name='remove_collect'),
    path('PostList/collected_posts/', collected_posts, name='collected_posts'),
    path('post/<int:post_id>/comment/', new_comment, name='new_comment'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('post/<int:post_id>/comment/<int:comment_id>/reply/', new_reply, name='new_reply'),
    path('reply/delete/<int:reply_id>/', delete_reply, name='delete_reply'),
]


