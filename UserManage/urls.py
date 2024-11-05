from django.urls import include, path
from . import views
app_name = "user_page"

urlpatterns = [
    path("", views.user_page, name='user_page'),
]
