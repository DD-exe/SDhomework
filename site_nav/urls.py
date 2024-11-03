from django.urls import path

from . import views

app_name = "site_nav"
urlpatterns = [
    # 信息安全网站导航页面
    path("", views.site_nav, name="default"),

    # 网站列表
    path("site/list/", views.site_nav_list, name="site-list"),
    # 添加网站
    path("site/add/", views.site_nav_add, name="site-add"),
    # 编辑网站
    path("site/<int:id>/edit/", views.site_nav_edit, name="site-edit"),
    # 删除网站
    path("site/<int:id>/delete/", views.site_nav_delete, name="site-delete"),

    # 分类列表
    path("categ/list/", views.site_categ_list, name="categ-list"),
    # 添加分类
    path("categ/add/", views.site_categ_add, name="categ-add"),
    # 编辑分类
    path("categ/<int:id>/edit/", views.site_categ_edit, name="categ-edit"),
    # 删除分类
    path("categ/<int:id>/delete/", views.site_categ_delete, name="categ-delete"),
]

from .config import IS_SITE_NAV_TEST
if IS_SITE_NAV_TEST:
    from .tests.common import login, logout
    urlpatterns += [
        # 模拟登录
        path("login/", login, name="login"),
        # 模拟注销
        path("logout/", logout, name="logout"),
    ]
