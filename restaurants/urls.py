from django.urls import path
from . import views
from accounts import views as accounts_views


urlpatterns = [
    path('', accounts_views.restaurant_profile, name='restaurant'),
    path('owner/', views.my_restaurant_profile, name='my_restaurant_profile'),
    path('menu_builder/', views.menu_builder, name='menu_builder'),
    path('menu_builder/category/<int:pk>/', views.products_by_category, name='products_by_category'),
    # Category
    path('menu_builder/category/add/', views.add_category, name='add_category'),
    path('menu_builder/category/edit/<int:pk>', views.edit_category, name='edit_category'),
    path('menu_builder/category/delete/<int:pk>', views.delete_category, name='delete_category'),
    # Products Food
]
