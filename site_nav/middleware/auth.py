from django.shortcuts import redirect
from django.urls import reverse

from ..models import SiteCategory, SiteNav
from .. import views
from ..utils import utils
from ..config import UserAPI

# 在“root.html”中的参数，在中间件的`process_template_response`中赋值



class LoginMiddleware:
    '''
    登录中间件

    判断用户是否登录，若未登录且访问了必须要登录的地址，则重定向到登录界面。

    对于视图函数返回的`TemplateResponse`添加部分登录相关的渲染参数，用来区分未登录和已登录的html界面，从而减少html模板和视图函数的编写。
    '''
    # 登录可访问的地址
    loggedin_views = [views.site_nav_list, views.site_nav_add, views.site_nav_edit, views.site_nav_delete,
                      views.site_categ_list, views.site_categ_add, views.site_categ_edit, views.site_categ_delete]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # 用于判断用户是否登录，若为None，则未登录
        self.user = UserAPI(request).user

        # request被向后传递
        # `process_template_response` 在内部被调用，因此无需显式地调用`process_template_response`
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not self.user.is_authenticated and view_func in self.loggedin_views:
            return redirect(reverse(UserAPI.login_url_name()))

    def process_template_response(self, request, response):
        '''
        添加渲染参数：loggedin, user

        中间件的hook函数，django自动调用，无需显式地调用

        对于视图函数返回的`TemplateResponse`添加部分登录相关的渲染参数，用来区分未登录和已登录的html界面，从而减少html模板和视图函数的编写

        若视图函数返回`HttpResponse`，则此函数不会被调用，因此如果希望此函数被调用，需要修改视图函数返回对象
        '''

        if response.context_data is None:
            response.context_data = {"user": self.user}
        else:
            response.context_data.setdefault("user", self.user)
        return response


class AdminMiddleware:
    '''
    判断是否是管理员访问敏感路径
    '''

    admin_paths = [reverse("site_nav:site-list"), reverse("site_nav:categ-list")]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        user = UserAPI(request).user
        # 试图访问管理员权限的路径，且不是管理员
        if request.path_info in self.admin_paths and (user.id is None or not user.is_superuser):
            return redirect(reverse(UserAPI.login_url_name()))

        # request被向后传递
        # `process_template_response` 在内部被调用，因此无需显式地调用`process_template_response`
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response


class UserMiddleware:
    '''
    判断路径中的id数据是否是此用户的数据
    '''
    
    site_nav_views = [views.site_nav_delete, views.site_nav_edit]
    site_categ_views = [views.site_categ_delete, views.site_categ_edit]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # request被向后传递
        # `process_template_response` 在内部被调用，因此无需显式地调用`process_template_response`
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func not in self.site_nav_views and view_func not in self.site_categ_views:
            # 不是访问敏感路径
            return

        user = UserAPI(request).user
        if user.is_superuser:
            # 管理员可随意修改
            return

        data_id = view_kwargs.get("id")
        if data_id is not None:
            if view_func in self.site_nav_views:
                data = SiteNav.objects.filter(id=data_id).first()
                if data is not None and user.id == data.user_id:
                    return 
            else: # view_func in self.site_categ_views
                data = SiteCategory.objects.filter(id=data_id).first()
                if data is not None and user.id == data.user_id:
                    return                
        # 用户试图修改或删除非自己的数据
        return redirect(reverse("site_nav:default"))
