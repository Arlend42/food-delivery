from .models import User


def determine_user(user):
    if user.role == User.RESTAURANT:
        redirectUrl = 'restaurant_profile'
        return redirectUrl
    elif user.role == User.CUSTOMER:
        redirectUrl = 'customer_profile'
        return redirectUrl
    elif user.role is None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
