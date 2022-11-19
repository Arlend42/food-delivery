from django.urls import path
from . import views
urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:restaurant_slug>', views.restaurant_detail, name='restaurant_detail')
]
