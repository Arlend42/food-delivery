from django.urls import path
from . import views


urlpatterns = [
    path("register_user/", views.register_user, name="register_user"),
    path(
        "register_restaurants/", views.register_restaurants, name="register_restaurants"
    ),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('my_account/', views.my_account, name='my_account'),
    path('customer_profile/', views.customer_profile, name='customer_profile'),
    path('restaurant_profile/', views.restaurant_profile, name='restaurant_profile')
]
