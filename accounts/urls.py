from django.urls import path
from . import views


urlpatterns = [
    path("register_user/", views.register_user, name="register_user"),
    path(
        "register_restaurants/", views.register_restaurants, name="register_restaurants"
    ),
]
