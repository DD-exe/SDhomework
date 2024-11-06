from django.urls import path

from . import views

app_name = "txtencoder"
urlpatterns = [
    path("", views.index, name="index"),
]
