from django.urls import include, path
from . import views
app_name = "user_page"

urlpatterns = [
    path("", views.user_page, name='user_page'),
    path("edit/",views.user_edit, name='user_edit'),
    path("post/",views.user_post, name='user_post'),
    path("comment/",views.user_comment, name='user_comment'),
    path("reply/",views.user_reply, name='user_reply'),
    path("favpost/",views.fav_post, name='fav_post'),
]
