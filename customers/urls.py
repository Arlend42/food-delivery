from django.urls import path
from accounts import views as account_views
from . import views


urlpatterns = [
    path('', account_views.customer_profile, name='customer_profile'),
    path('profile/', views.c_profile, name='c_profile'),
]