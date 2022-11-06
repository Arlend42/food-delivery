from django.urls import path

from . import views


urlpatterns = [
    path("config/", views.get_config, name="payments-config"),
    path("success/", views.get_payment_success, name="payments-success"),
    path("cancel/", views.get_payment_cancel, name="payments-cancel"),
    path("checkout/", views.get_checkout_session, name="payments-checkout"),
    path("cart/", views.get_shopping_cart, name="payments-cart"),
]
