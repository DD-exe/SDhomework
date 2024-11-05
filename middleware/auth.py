from django.shortcuts import redirect
from django.urls import reverse, resolve

from UserManage.views import img_code
from site_nav.models import SiteCategory, SiteNav
from site_nav import views
from site_nav.utils import utils
from site_nav.config import UserAPI

import file_encoder.views
import txtencoder.views
import forum.views
import UserManage.views

class InfoMiddleware:
    '''
    对所有用户（包括未登录用户）进行普通的信息收集储存。目前主要是保存用户的上一个url和用户配置。

    “用户的上一个url”定义：
    1. 请求的不是静态文件，即该请求将要调用各个app的视图函数;
    2. 与当前url不同的最近的一个url。

    要使用“用户的上一个url”的功能：
    1. 场景1：在视图函数中使用。直接使用`request.session["info"]["last_url"]`，可直接redirect；
    2. 场景2：在templates的html中使用。
        1. 方法1（推荐）：html中：`{{ last_url }}`；views中；将html对应的函数中的`render`改为`TemplateResponse`。
           原理：渲染参数在`InfoMiddleware.process_template_response`中被传入；
        2. 方法2：直接从视图函数中传入html的渲染参数。

    对于视图函数返回的`TemplateResponse`添加渲染参数，从而减少html模板和视图函数的编写。

    最好优先执行此中间件，以免在执行此中间件前被其他中间件拦截request。
    '''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        views_dir = (dir(views) + dir(file_encoder.views) + dir(txtencoder.views) + dir(forum.views))
        views_dir.append('my_login')
        views_dir.append('log_out')
        if resolve(request.path_info).func.__name__ in views_dir:
            # 若不是访问静态页面，而是访问正常网页调用视图函数，则正常赋值
            # 若没有，则创建
            utils.set_default_session(request.session, "info",{"current_url": request.path_info, "last_url": reverse("site_nav:default")})
            #lasr_url默认值需要改成主页
            # 只有不同才改
            if request.session["info"]["current_url"] != request.path_info:

                utils.update_session(request.session, "info", {"current_url": request.path_info,"last_url": request.session["info"]["current_url"]})
            print(request.session["info"]["current_url"], request.session["info"]["last_url"])
        else:
            utils.set_default_session(request.session, "info", {"current_url": reverse("site_nav:default"),"last_url": reverse("site_nav:default")})

        # config
        utils.set_default_session(request.session, "config", {"display": "all_display"})

        # request被向后传递
        # `process_template_response` 在内部被调用，因此无需显式地调用`process_template_response`
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_template_response(self, request, response):
        '''
        添加渲染参数：last_url, display

        中间件的hook函数，django自动调用，无需显式地调用

        对于视图函数返回的`TemplateResponse`添加部分登录相关的渲染参数，用来区分未登录和已登录的html界面，从而减少html模板和视图函数的编写

        若视图函数返回`HttpResponse`，则此函数不会被调用，因此如果希望此函数被调用，需要修改视图函数返回对象
        '''

        if response.context_data is None:
            response.context_data = {"last_url": request.session["info"]["last_url"],
                                     "config_display": request.session["config"]["display"]}
        else:
            response.context_data.setdefault("last_url", request.session["info"]["last_url"])
            display = request.session["config"]["display"]
            config_display = [True, False, False]
            if display == "default_display":
                config_display = [False, True, False]
            elif display == "user_display":
                config_display = [False, False, True]
            response.context_data.setdefault("config_display", config_display)
        return response