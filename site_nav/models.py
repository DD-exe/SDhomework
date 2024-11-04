from django.db import models
from django.urls import reverse
from django.core import validators
from django.core.exceptions import ValidationError

from .utils import utils
# used in the foreign key of the 2 models
from .config import User


class SiteCategory(models.Model):
    '''
    网站分类表
    '''

    # 不支持多主码，使用unique_together
    # 主码：(user_id, name)
    # 外码：user_id
    user = models.ForeignKey(
        verbose_name="用户", to="User", to_field="id", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="分类名", max_length=64)
    # 用于排序
    weight = models.IntegerField(verbose_name="分类的权重", default=0, blank=True)
    description = models.TextField(
        verbose_name="分类的描述", max_length=200, default="", blank=True)
    # TODO: 分类的图标

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        # unique_together = ("user_id", "name")
        constraints = [
            models.UniqueConstraint(
                name="unique_name_user", fields=("user", "name")),
        ]
        ordering = ["-weight", "user", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("SiteCategory_detail", kwargs={"pk": self.pk})

    def clean(self):
        ret = super().clean()
        if self.weight is None:
            self.weight = SiteCategory.weight.default
        if self.description is None:
            self.description = SiteCategory.description.default
        return ret

    @staticmethod
    def fields_to_use():
        '''
        此表中可以展现给用户的字段。也影响着表单。
        '''
        return ["id", "user", "name", "weight", "description"]

    @classmethod
    def fields(cls):
        '''
        返回字典，以字段名称为key，以模型字段对象为value。

        用途与`fields2dict`有本质区别。`fields`是类方法，且返回的字典value仍是`django.db.models.Field`的子类，可以访问`verbose_name`等有用的选项。
        而`field2dict`返回的字典value是字段的值。
        '''
        return {value.name: value for value in cls._meta.get_fields() if value.name in cls.fields_to_use()}

    def _fields2dict(self):
        return {"id": self.id, "user": self.user, "name": self.name, "weight": self.weight, "description": self.description}

    def fields2dict(self):
        '''
        将`fiels_to_use()`返回的字段作为字典的key，并将字段的值作为字典的value
        '''
        return {key: value for key, value in self._fields2dict().items() if key in self.fields_to_use()}


class SiteNav(models.Model):
    '''
    网站表
    '''

    # 主码：(user_id, url)
    # 外码：user_id, category
    user = models.ForeignKey(
        verbose_name="用户", to="User", to_field="id", on_delete=models.CASCADE)
    category = models.ForeignKey(verbose_name="网站的分类", to="SiteCategory",
                                 to_field="id", on_delete=models.CASCADE)
    url = models.URLField(verbose_name="网站链接")
    backup_url = models.URLField(verbose_name="网站备用链接", default="", blank=True)
    name = models.CharField(
        verbose_name="网站名", max_length=64, default="", blank=True)
    # 用于排序
    weight = models.IntegerField(verbose_name="网站的权重", default=0, blank=True)
    description = models.TextField(
        verbose_name="网站的描述", max_length=200, default="", blank=True)

    class Meta:
        verbose_name = "网站"
        verbose_name_plural = "网站"
        # unique_together = ("user_id", "url")
        constraints = [
            models.UniqueConstraint(
                name="unique_url_user", fields=("user", "url")),
        ]
        ordering = ["-weight", "user", "url"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("SiteNav_detail", kwargs={"pk": self.pk})

    def clean(self):
        ret = super().clean()
        if self.category_id is None:
            self.category_id = SiteNav.category.field.default
        if self.backup_url is None:
            self.backup_url = SiteNav.backup_url.default
        if self.name is None:
            self.name = SiteNav.name.default
        if self.weight is None:
            self.weight = SiteNav.weight.default
        if self.description is None:
            self.description = SiteNav.description.default

        # special
        if self.name == "":
            # 必须先检查url正确性
            try:
                validators.URLValidator(self.url)
            except ValidationError as e:
                raise e
            
            # name max length: 64
            self.name = utils.get_title(self.url)[:64]
        return ret

    @staticmethod
    def fields_to_use():
        '''
        此表中可以展现给用户的字段。也影响着表单。
        '''
        return ["id", "user", "url", "backup_url", "name", "weight", "description", "category"]

    @classmethod
    def fields(cls):
        '''
        返回字典，以字段名称为key，以模型字段对象为value

        用途与`fields2dict`有本质区别。`fields`是类方法，且返回的字典value仍是`django.db.models.Field`的子类，可以访问`verbose_name`等有用的选项。
        而`field2dict`返回的字典value是字段的值。
        '''
        return {value.name: value for value in cls._meta.get_fields() if value.name in cls.fields_to_use()}

    def _fields2dict(self):
        return {"id": self.id, "user": self.user, "url": self.url, "backup_url": self.backup_url, "name": self.name, "weight": self.weight, "description": self.description, "category": self.category}

    def fields2dict(self):
        '''
        将`fiels_to_use()`返回的字段作为字典的key，并将字段的值作为字典的value
        '''
        return {key: value for key, value in self._fields2dict().items() if key in self.fields_to_use()}
