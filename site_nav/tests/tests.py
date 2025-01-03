from django.test import TestCase

from ..config import IS_SITE_NAV_TEST

if IS_SITE_NAV_TEST:
    from django.db import models
    from django.urls import reverse


    class User(models.Model):
        '''
        用户表
        '''

        id = models.BigAutoField(verbose_name="用户ID", primary_key=True)
        name = models.CharField(verbose_name="用户名", max_length=64)

        class Meta:
            verbose_name = "用户"
            verbose_name_plural = "用户"

        # 重定义print内容
        def __str__(self):
            return self.name

        # 重定义内置方法，用于灵活地得到url，有利于html模板
        def get_absolute_url(self):
            # 反向解析url
            return reverse("User_detail", kwargs={"pk": self.pk})

    class _User():
        def __init__(self, request, admin_ids):
            self.request = request
            self._admin_ids = admin_ids

        @property
        def id(self):
            return self.request.session.get("user", dict()).get("id")
        
        @property
        def username(self):
            return self.request.session.get("user", dict()).get("name")

        @property
        def is_authenticated(self):
            return self.request.session.get("user") is not None

        @property
        def is_superuser(self):
            return self.id in self._admin_ids    


    class UserAPI():
        _admin_ids = [1]
        _default_ids = [1]

        def __init__(self, request):
            self.request = request

        @property
        def user(self):
            return _User(request, _admin_ids)

        @staticmethod
        def login_url_name():
            return "site_nav:login"

        @staticmethod
        def logout_url_name():
            return "site_nav:logout"

        @staticmethod
        def default_user_ids():
            return _default_ids

