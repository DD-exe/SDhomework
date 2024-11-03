from ..config import IS_SITE_NAV_TEST

if IS_SITE_NAV_TEST:
    from django import forms
    from django.template.response import TemplateResponse
    from django.urls import reverse
    from django.shortcuts import redirect
    from django.urls import path

    from .tests import User, UserAPI

    def login(request):
        if request.method == "GET":
            form = LoginForm()
            return TemplateResponse(request, "login.html", {"form": form})

        elif request.method == "POST":
            form = LoginForm(data=request.POST)
            if form.is_valid():
                obj = User.objects.filter(**form.cleaned_data).first()
                if obj is not None:
                    # 模拟登录成功
                    # 添加session数据
                    # user: 用户相关信息
                    #     id: 用户id
                    #     name: 用户名
                    request.session["user"] = {"id": obj.id, "name": obj.name}
                    return redirect(request.session["info"]["last_url"])
                else:
                    form.add_error(None, "登录失败")
                    return TemplateResponse(request, "login.html", {"form": form})
            else:
                return TemplateResponse(request, "login.html", {"form": form, "was_validated": "was-validated"})


    def logout(request):
        request.session.flush()
        return redirect(reverse(UserAPI.login_url_name()))


    # try to fix the "circular import" problem
    from ..views import BootStrapForm
    class LoginForm(BootStrapForm):
        name = forms.CharField(
            label="用户名", widget=forms.TextInput(), max_length=64)
