from django.urls import path
from . import views


urlpatterns = [
    path("register_user/", views.register_user, name="register_user"),
    path(
        "register_restaurants/", views.register_restaurants, name="register_restaurants"
    ),
    path('login/', views.login, name='login'),
    path('logout/', views.login, name='logout'),
    path('dashboard', views.dashboard, name='dashboard')
]
