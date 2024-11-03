from django.urls import path

from app import views 
 32  
 31 urlpatterns = [ 
 30     # path("admin/", admin.site.urls), 
 29     re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}), 
 28     # 模拟登录 
 27     path("login/", views.login, name="app-login"), 
 26     # 模拟注销 
 25     path("logout/", views.logout, name="app-logout"), 
 24  
 23     # 信息安全网站导航页面 
 22     path("site/nav/", views.site_nav, name="app-site-nav"), 
 21  
 20     # 网站列表 
 19     path("site/nav/list/", views.site_nav_list, name="app-site-nav-list"), 
 18     # 添加网站 
 17     path("site/nav/add/", views.site_nav_add, name="app-site-nav-add"), 
 16     # 编辑网站 
 15     path("site/nav/<int:id>/edit/", views.site_nav_edit, name="app-site-nav-edit"), 
 14     # 删除网站 
 13     path("site/nav/<int:id>/delete/", views.site_nav_delete, name="app-site-nav-delete"), 
 12  
 11     # 分类列表 
 10     path("site/categ/list/", views.site_categ_list, name="app-site-categ-list"), 
  9     # 添加分类 
  8     path("site/categ/add/", views.site_categ_add, name="app-site-categ-add"), 
  7     # 编辑分类 
  6     path("site/categ/<int:id>/edit/", views.site_categ_edit, name="app-site-categ-edit"), 
  5     # 删除分类 
  4     path("site/categ/<int:id>/delete/", views.site_categ_delete, name="app-site-categ-delete"), 
  3  
  2     # 备用的参考的网站导航页面 
  1     path("backup/site/nav/", views.backup_site_nav, name="app-backup-site-nav"), 
54  ] 
