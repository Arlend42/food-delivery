from django.urls import path
from . import views

urlpatterns = [
    path("", views.marketplace, name="marketplace"),
    path("<slug:restaurant_slug>", views.restaurant_detail, name="restaurant_detail"),
    # ADD to CART
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    # Remove from CART
    path("remove_from_cart/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    # Delete cart item
    path('delete_cart_item/<int:cart_id>/', views.delete_cart_item, name="delete_cart_item"),
]
