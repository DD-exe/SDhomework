from django.shortcuts import redirect, HttpResponse
from django.urls import reverse, resolve
from app.models import User, SiteCategory, SiteNav, ADMIN_ID
from app import views
from app.utils import utils

# 在“root.html”中的参数，在中间件的`process_template_response`中赋值


class InfoMiddleware:
    '''
    对所有用户（包括未登录用户）进行普通的信息收集储存。目前主要是保存用户的上一个url。
    
    为了对未登录用户起作用，要在LoginMiddleware前执行。
    '''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if resolve(request.path_info).func.__name__ in dir(views):
            # 若不是访问静态页面，而是访问正常网页调用视图函数，则正常赋值

            print("0: ", request.session.get("info"))
            # 若没有，则创建
            utils.set_default_session(request.session, "info", {"current_url": request.path_info, "last_url": reverse("app-site-nav")})
            print("1: ", request.session.get("info"))
            # 只有不同才改
            if request.session["info"]["current_url"] != request.path_info:
                utils.update_session(request.session, "info", {"current_url": request.path_info, "last_url": request.session["info"]["current_url"]})
                print("3: ", request.session.get("info"))
        else:
            utils.set_default_session(request.session, "info", {"current_url": reverse("app-site-nav"), "last_url": reverse("app-site-nav")})
        
        print("4: ", request.session.get("info"))
        # config
        utils.set_default_session(request.session, "config", {"display": "all_display"})
        print(request.session.get("config"))

        # request被向后传递
        # `process_template_response` 在内部被调用，因此无需显式地调用`process_template_response`
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_template_response(self, request, response):
        '''
        中间件的hook函数，django自动调用，无需显式地调用

        对于视图函数返回的`TemplateResponse`添加部分登录相关的渲染参数，用来区分未登录和已登录的html界面，从而减少html模板和视图函数的编写

        若视图函数返回`HttpResponse`，则此函数不会被调用，因此如果希望此函数被调用，需要修改视图函数返回对象
        '''
        
        print("6: ", request.session.get("info"))
        if response.context_data is None:
            response.context_data = {"last_url": request.session["info"]["last_url"], "display": request.session["config"]["display"]}
        else:
            response.context_data.setdefault("last_url", request.session["info"]["last_url"]) 
            display = request.session["config"]["display"] 
            config_display = [True, False, False]
            if display == "default_display":
                config_display = [False, True, False]
            elif display == "user_display":
                config_display = [False, False, True]
            response.context_data.setdefault("config_display", config_display) 
            print(config_display)
        return response


class LoginMiddleware:
    '''
    登录中间件

    判断用户是否登录，若未登录且访问了必须要登录的地址，则重定向到登录界面

    此外，对于视图函数返回的`TemplateResponse`添加部分登录相关的渲染参数，用来区分未登录和已登录的html界面，从而减少html模板和视图函数的编写
    '''

    # 未登录可访问的地址
    except_paths = [reverse("app-login"), reverse("app-site-nav"),
                    reverse("app-logout"), reverse("app-backup-site-nav")]

    def __init__(self, get_response):
        self.loggedin = False
        self.user = dict()
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # 用于判断用户是否登录，若为None，则未登录
        self.user = request.session.get("user", {})
        self.loggedin = True if self.user != {} else False
        if not self.loggedin and request.path_info not in self.except_paths:
            return redirect(reverse("app-login"))

        # request被向后传递
        # `process_template_response` 在内部被调用，因此无需显式地调用`process_template_response`
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_template_response(self, request, response):
        '''
        中间件的hook函数，django自动调用，无需显式地调用

        对于视图函数返回的`TemplateResponse`添加部分登录相关的渲染参数，用来区分未登录和已登录的html界面，从而减少html模板和视图函数的编写

        若视图函数返回`HttpResponse`，则此函数不会被调用，因此如果希望此函数被调用，需要修改视图函数返回对象
        '''

        if response.context_data is None:
            response.context_data = {"loggedin": self.loggedin, "user": self.user, "ADMIN_ID": ADMIN_ID}
        else:
            response.context_data.setdefault("loggedin", self.loggedin)
            response.context_data.setdefault("user", self.user)
            response.context_data.setdefault("ADMIN_ID", ADMIN_ID)
        return response


class AdminMiddleware:
    '''
    判断是否是管理员访问敏感路径
    '''

    admin_paths = [reverse("app-site-nav-list"), reverse("app-site-categ-list")]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        user = request.session.get("user", dict())
        user_id = user.get("id")
        # 试图访问管理员权限的路径，且不是管理员
        if request.path_info in self.admin_paths and (user_id is None or user_id not in ADMIN_ID):
            return redirect(reverse("app-site-nav"))

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

        user = request.session.get("user", dict())
        user_id = user.get("id")
        if user_id is None:
            # 未登录
            return redirect(reverse("app-login"))

        if user_id in ADMIN_ID:
            # 管理员可随意修改
            return

        data_id = view_kwargs.get("id")
        if data_id is not None:
            if view_func in self.site_nav_views:
                data = SiteNav.objects.filter(id=data_id).first()
                if data is not None and user_id == data.user_id:
                    return 
            else: # view_func in self.site_categ_views
                data = SiteCategory.objects.filter(id=data_id).first()
                if data is not None and user_id == data.user_id:
                    return                
        # 用户试图修改或删除非自己的数据
        return redirect(reverse("app-site-nav"))
