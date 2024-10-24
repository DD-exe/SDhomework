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
from django.urls import path, re_path
from django.views.static import serve
from web_project import settings
from app import views

urlpatterns = [
    # path("admin/", admin.site.urls),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    # 模拟登录
    path("login/", views.login, name="app-login"),
    # 模拟注销
    path("logout/", views.logout, name="app-logout"),

    # 信息安全网站导航页面
    path("site/nav/", views.site_nav, name="app-site-nav"),

    # 网站列表
    path("site/nav/list/", views.site_nav_list, name="app-site-nav-list"),
    # 添加网站
    path("site/nav/add/", views.site_nav_add, name="app-site-nav-add"),
    # 编辑网站
    path("site/nav/<int:id>/edit/", views.site_nav_edit, name="app-site-nav-edit"),
    # 删除网站
    path("site/nav/<int:id>/delete/", views.site_nav_delete, name="app-site-nav-delete"),

    # 分类列表
    path("site/categ/list/", views.site_categ_list, name="app-site-categ-list"),
    # 添加分类
    path("site/categ/add/", views.site_categ_add, name="app-site-categ-add"),
    # 编辑分类
    path("site/categ/<int:id>/edit/", views.site_categ_edit, name="app-site-categ-edit"),
    # 删除分类
    path("site/categ/<int:id>/delete/", views.site_categ_delete, name="app-site-categ-delete"),

    # 备用的参考的网站导航页面
    path("backup/site/nav/", views.backup_site_nav, name="app-backup-site-nav"),
]
