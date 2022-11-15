from django.urls import path
from . import views
from accounts import views as accounts_views


urlpatterns = [
    path('', accounts_views.restaurant_profile, name='restaurant'),
    path('owner/', views.my_restaurant_profile, name='my_restaurant_profile'),
]
