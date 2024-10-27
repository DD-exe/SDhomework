from urllib.parse import urlparse
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect, HttpResponse
from django import forms
from django.urls import reverse, resolve
from django.template.response import TemplateResponse
from app.models import User, SiteCategory, SiteNav, IS_APP_DEBUG, ADMIN_ID
from app.utils import utils


def add_classes(form, fields: list | str = "__all__", classes_to_add: str | dict = {"input_class": "form-control", "select_class": "form-select"}) -> None:
    '''
    为表单增加html属性class, 用于html模板渲染
    '''
    if isinstance(classes_to_add, str):
        input_class = select_class = classes_to_add
    elif isinstance(classes_to_add, dict):
        input_class = classes_to_add.get("input_class", "")
        select_class = classes_to_add.get("select_class", "")
    else:
        return

    # 循环添加属性
    for name, field in form.fields.items():
        if fields != "__all__" and name not in fields:
            continue

        # 若已有属性，则保留原来其他属性；若无属性，创建属性
        if hasattr(field.widget, "attrs"):
            field.widget.attrs["placeholder"] = field.label
            if "class" in field.widget.attrs:
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs["class"] += " " + select_class
                else:
                    field.widget.attrs["class"] += " " + input_class
            else:
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs["class"] = select_class
                else:
                    field.widget.attrs["class"] = input_class
        else:
            field.widget.attrs = {"placeholder": field.label}
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = select_class
            else:
                field.widget.attrs["class"] = input_class


def remove_classes(form, fields: list | str = "__all__", classes_to_remove: list = []) -> None:
    '''
    为表单去除html属性class中的值, 用于html模板渲染
    '''
    for name, field in form.fields.items():
        if fields != "__all___" and name not in fields:
            continue
        # 若已有属性，则保留原来其他属性；若无属性，创建属性
        if hasattr(field.widget, "attrs"):
            if "class" in field.widget.attrs:
                for cls in classes_to_remove:
                    field.widget.attrs["class"].replace(cls, "")


def constrain_select(self, constraints: dict = dict()) -> None:
    '''
    对下拉选择框中的内容进行限制

    Args:
        constraints (dict(dict)): 字典的字典，key是限制的字段名，value是查询该字段依赖的数据库时应用的过滤条件（以字典的形式）
    '''
    for name, constraint in constraints.items():
        if name in self.fields:
            field = self.fields[name]
            if isinstance(field.widget, forms.Select):
                field.queryset = field.queryset.filter(**constraint)


class BootStrapModelForm(forms.ModelForm):
    # register fields to be checked by the server side instead of the client side, static
    server_side_fields = []

    def __init__(
        self,
        classes_to_add={"input_class": "form-control",
                        "select_class": "form-select"},
        data=None,
        files=None,
        auto_id="id_%s",
        prefix=None,
        initial=None,
        error_class=ErrorList,
        label_suffix=None,
        empty_permitted=False,
        instance=None,
        use_required_attribute=None,
        renderer=None,
    ):
        super().__init__(
            data,
            files,
            auto_id,
            prefix,
            initial,
            error_class,
            label_suffix,
            empty_permitted,
            instance,
            use_required_attribute,
            renderer,
        )
        add_classes(
            self, "__all__", classes_to_add)

        # 为sever_side_fields添加aria_describedby属性，从而能显示`.invalid-feedback`的错误信息。
        # 注意：这也是html模板中`.invalid-feedback`的错误信息的id，要加上
        for name, field in self.fields.items():
            if name in self.server_side_fields:
                if "aria_describedby" not in field.widget.attrs:
                    field.widget.attrs["aria_describedby"] = name + \
                        "ServerValidationFeedback"
                else:
                    field.widget.attrs["aria_describedby"] += " " + name + \
                        "ServerValidationFeedback"

    def is_valid(self) -> bool:
        '''
        在调用父类方法后，为server_side_field加上是否valid的html class。
        
        注意：子类ModelForm通常还要覆盖此方法，进行进一步数据库的full_clean操作，从而判断最终是否valid
        '''
        if super().is_valid():
            remove_classes(self, self.server_side_fields, "is-invalid")
            add_classes(self, self.server_side_fields, "is-valid")
            return True
        else:
            for field_name in self.server_side_fields:
                if field_name in self.errors:
                    remove_classes(self, [field_name], "is-valid")
                    add_classes(self, [field_name], "is-invalid")


class BootStrapForm(forms.Form):
    def __init__(
        self,
        classes_to_add={"input_class": "form-control",
                        "select_class": "form-select"},
        data=None,
        files=None,
        auto_id="id_%s",
        prefix=None,
        initial=None,
        error_class=ErrorList,
        label_suffix=None,
        empty_permitted=False,
        field_order=None,
        use_required_attribute=None,
        renderer=None,
    ):
        super().__init__(
            data,
            files,
            auto_id,
            prefix,
            initial,
            error_class,
            label_suffix,
            empty_permitted,
            field_order,
            use_required_attribute,
            renderer,
        )
        add_classes(
            self, "__all__", classes_to_add)


class UserForm(BootStrapModelForm):
    class Meta:
        model = User
        fields = ["name"]


class SiteCategoryOriginForm(BootStrapModelForm):
    server_side_fields = ["name"]

    class Meta:
        model = SiteCategory
        fields = ["name", "weight", "description"]

    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
        super().__init__(*args, **kwargs)

    def is_valid(self) -> bool:
        '''
        检查表单字段后，还要对要保存到数据库的Model进行检查
        '''
        if not super().is_valid():
            return False

        obj = super().save(commit=False)
        obj.user_id = self.user_id
        try:
            obj.full_clean()
            remove_classes(self, self.server_side_fields, "is-invalid")
            add_classes(self, self.server_side_fields, "is-valid")
            return True
        except Exception as e:
            self.add_error("name", "分类 已经存在")
            remove_classes(self, self.server_side_fields, "is-valid")
            add_classes(self, self.server_side_fields, "is-invalid")
            return False

    def save(self, commit=True):
        '''
        填充表单中不存在的字段后再保存
        '''
        obj = super().save(commit=False)
        obj.user_id = self.user_id

        if commit:
            obj.save()
        else:
            return obj


class SiteCategoryAdminForm(BootStrapModelForm):
    server_side_fields = ["user", "name"]

    class Meta:
        model = SiteCategory
        fields = "__all__"


def SiteCategoryForm(user_id, *args, **kwargs):
    return SiteCategoryOriginForm(user_id, *args, **kwargs) if user_id not in ADMIN_ID else SiteCategoryAdminForm(*args, **kwargs)


class SiteNavOriginForm(BootStrapModelForm):
    server_side_fields = ["url"]

    class Meta:
        model = SiteNav
        fields = ["url", "backup_url", "name",
                  "category", "weight", "description"]

    def __init__(
        self,
        user_id,
        constraints=dict(),
        classes_to_add={"input_class": "form-control",
                        "select_class": "form-select"},
        data=None,
        files=None,
        auto_id="id_%s",
        prefix=None,
        initial=None,
        error_class=ErrorList,
        label_suffix=None,
        empty_permitted=False,
        instance=None,
        use_required_attribute=None,
        renderer=None,
    ):
        '''
        Args:
            user_id: 当前用户的id，用于限制下拉选择框的内容。
                     `user_id=id` 解析为 `constraints={"category": {"user_id__in": [id, ADMIN_ID[0]]}, <other constraints>}`
            constraints (dict): `constrain_select`参数
        '''
        super().__init__(
            classes_to_add,
            data,
            files,
            auto_id,
            prefix,
            initial,
            error_class,
            label_suffix,
            empty_permitted,
            instance,
            use_required_attribute,
            renderer,
        )
        self.user_id = user_id
        if "category" not in constraints:
            # ADMIN_ID[0]: 包含默认用户的分类
            constraints["category"] = {"user_id__in": [user_id, ADMIN_ID[0]]}
        elif "user_id__in" not in constraints["category"]:
            constraints["category"]["user_id__in"] = [user_id, ADMIN_ID[0]]
        constrain_select(self, constraints)

    def is_valid(self) -> bool:
        '''
        检查表单字段后，还要对要保存到数据库的Model进行检查
        '''
        if not super().is_valid():
            return False

        obj = super().save(commit=False)
        obj.user_id = self.user_id
        try:
            obj.full_clean()
            remove_classes(self, self.server_side_fields, "is-invalid")
            add_classes(self, self.server_side_fields, "is-valid")
            return True
        except Exception as e:
            # 违反unique constriants
            self.add_error("url", "网站链接 已经存在")
            remove_classes(self, self.server_side_fields, "is-valid")
            add_classes(self, self.server_side_fields, "is-invalid")
            return False

    def save(self, commit=True):
        '''
        填充表单中不存在的字段后再保存
        '''
        obj = super().save(commit=False)
        obj.user_id = self.user_id

        if commit:
            obj.save()
        else:
            return obj


class SiteNavAdminForm(BootStrapModelForm):
    class Meta:
        model = SiteNav
        fields = "__all__"


def SiteNavForm(user_id, constraints=dict(), *args, **kwargs):
    return SiteNavOriginForm(user_id, constraints, *args, **kwargs) if user_id not in ADMIN_ID else SiteNavAdminForm(*args, **kwargs)


class LoginForm(BootStrapForm):
    name = forms.CharField(
        label="用户名", widget=forms.TextInput(), max_length=64)


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
    return redirect(reverse("app-login"))


def site_nav(request):
    if request.method == "GET":
        # 获取当前用户id，id为ADMIN_ID[0]表示默认用户，显示未登录可以显示的信息
        id_filter = []

        id_filter.append(ADMIN_ID[0])

        user = request.session.get("user", dict())
        user_id = user.get("id")
        if user_id is not None:
            id_filter.append(user_id)

        site_categ_query = SiteCategory.objects.filter(user__in=id_filter)
        site_nav_query = SiteNav.objects.filter(user__in=id_filter)
        return TemplateResponse(request, "site_nav.html", {"site_categ_query": site_categ_query, "site_nav_query": enumerate(site_nav_query)})
    
    elif request.method == "POST":
        # 接收XMLHTTPRequest，不刷新页面
        # 接收config表单信息
        utils.update_session(request.session, "config", {"display": request.POST.get("config_display", "all_display")})
        return HttpResponse()


def site_nav_list(request):
    query = SiteNav.objects.all()
    return TemplateResponse(request, "site_list.html", {"name": SiteNav._meta.verbose_name, "query": query})


def site_nav_add(request):
    op_title = "新增网站"

    if request.method == "GET":
        form = SiteNavForm(user_id=request.session["user"]["id"])
        return TemplateResponse(request, "site_add_edit.html", {"form": form, "op_title": op_title})

    # 表单以POST形式提交
    elif request.method == "POST":
        form = SiteNavForm(
            user_id=request.session["user"]["id"], data=request.POST)

        if form.is_valid():
            form.save()
            # 重定向到查看页面
            # 使用reverse反向解析views的路径，更灵活
            return redirect(request.session["info"]["last_url"])
        else:
            return TemplateResponse(request, "site_add_edit.html", {"form": form, "op_title": op_title, "was_validated": "was-validated"})


def site_nav_edit(request, id):
    op_title = "编辑网站"
    obj = SiteNav.objects.filter(id=id).first()

    if request.method == "GET":
        form = SiteNavForm(user_id=request.session["user"]["id"], instance=obj)
        return TemplateResponse(request, "site_add_edit.html", {"form": form, "op_title": op_title})

    # 表单以POST形式提交
    elif request.method == "POST":
        # 与add区别是：`instance`
        form = SiteNavForm(
            user_id=request.session["user"]["id"], data=request.POST, instance=obj)

        if form.is_valid():
            form.save()
            # 重定向到查看页面
            # 使用reverse反向解析views的路径，更灵活
            return redirect(request.session["info"]["last_url"])
        else:
            return TemplateResponse(request, "site_add_edit.html", {"form": form, "op_title": op_title, "was_validated": "was-validated"})


def site_nav_delete(request, id):
    obj = SiteNav.objects.filter(id=id).first()
    if obj is not None:
        obj.delete()
    return redirect(request.session["info"]["last_url"])


def site_categ_list(request):
    query = SiteCategory.objects.all()
    return TemplateResponse(request, "site_list.html", {"name": SiteCategory._meta.verbose_name, "query": query})


def site_categ_add(request):
    op_title = "新增分类"

    if request.method == "GET":
        form = SiteCategoryForm(user_id=request.session["user"]["id"])
        return TemplateResponse(request, "site_add_edit.html", {"form": form, "op_title": op_title})

    # 表单以POST形式提交
    elif request.method == "POST":
        form = SiteCategoryForm(
            user_id=request.session["user"]["id"], data=request.POST)

        if form.is_valid():
            form.save()
            # 重定向到查看页面
            # 使用reverse反向解析views的路径，更灵活
            return redirect(request.session["info"]["last_url"])
        else:
            return TemplateResponse(request, "site_add_edit.html", {"form": form, "op_title": op_title, "was_validated": "was-validated"})


def site_categ_edit(request, id):
    op_title = "编辑分类"
    obj = SiteCategory.objects.filter(id=id).first()

    if request.method == "GET":
        form = SiteCategoryForm(
            user_id=request.session["user"]["id"], instance=obj)
        return TemplateResponse(request, "site_add_edit.html", {"form": form, "op_title": op_title})

    # 表单以POST形式提交
    elif request.method == "POST":
        # 与add区别是：`instance`
        form = SiteCategoryForm(
            user_id=request.session["user"]["id"], data=request.POST, instance=obj)

        if form.is_valid():
            form.save()
            # 重定向到查看页面
            # 使用reverse反向解析views的路径，更灵活
            user = request.session.get("user", dict())
            user_id = user.get("id")
            return redirect(request.session["info"]["last_url"])
        else:
            return TemplateResponse(request, "site_add_edit.html", {"form": form, "op_title": op_title, "was_validated": "was-validated"})


def site_categ_delete(request, id):
    obj = SiteCategory.objects.filter(id=id).first()
    if obj is not None:
        obj.delete()
    return redirect(request.session["info"]["last_url"])


def backup_site_nav(request):
    return TemplateResponse(request, "backup_site_categ.html")
