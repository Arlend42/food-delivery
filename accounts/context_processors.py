from django.conf import settings
from accounts.models import UserProfile
from restaurants.models import Restaurant


def get_restaurant(request):
    try:
        restaurant = Restaurant.objects.get(user=request.user)
    except:
        restaurant = None
    return dict(restaurant=restaurant)


def get_customer_profile(request):
    try:
        customer_profile = UserProfile.objects.get(user=request.user)
    except:
        customer_profile = None
    return dict(customer_profile=customer_profile)


def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}
