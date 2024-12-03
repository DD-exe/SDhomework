from django.contrib import admin

from .models import SiteCategory, SiteNav

# Register your models here.

admin.site.register(SiteCategory)
admin.site.register(SiteNav)

