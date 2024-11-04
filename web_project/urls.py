"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from UserManage import views
from web_project import settings

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("file_encoder/", include("file_encoder.urls")),
    path("txtencoder/", include("txtencoder.urls")),
    path('forum/', include('forum.urls')),
    path("sitenav/", include("site_nav.urls")),
    path('login/',views.my_login, name='login'),
    path('register/',views.register),
    path('alterpw/',views.alter_pw),
    path('forgetpw/',views.forget_pw),
    path('resetpw/',views.reset_pw),
    path('image/code/',views.img_code),
    path('active',views.account_activate),
    path('reset',views.password_reset),
    path('logout/', views.log_out, name='logout')
]


