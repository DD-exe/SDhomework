from django.urls import path

from . import views

app_name = "file_encoder"
urlpatterns = [
    path("", views.index, name="index"),
]
