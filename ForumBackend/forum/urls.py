# urls.py

from django.conf import settings
from django.conf.urls import include
from django.urls import path
from . import views
from .views import home, post_list, new_post, delete_post, edit_post, login_view, register_view

urlpatterns = [
    path('home/', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('PostList/', post_list, name='post_list'),
    path('NewPost/', new_post, name='new_post'),
    path('delete/<int:post_id>/', delete_post, name='delete_post'),
    path('EditPost/<int:post_id>/', edit_post, name='edit_post'),

    path('__debug__/', include('debug_toolbar.urls')),
]


if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]