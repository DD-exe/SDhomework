from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.Subject)
admin.site.register(models.Post)
admin.site.register(models.Collect)
admin.site.register(models.Comment)
admin.site.register(models.Reply)

