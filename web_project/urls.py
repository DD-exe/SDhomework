"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from UserManage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.my_login),
    path('register/',views.register),
    path('alterpw/',views.alter_pw),
    path('forgetpw/',views.forget_pw),
    path('resetpw/',views.reset_pw),
    path('image/code/',views.img_code),
    path('active',views.account_activate),
    path('reset',views.password_reset)
]
