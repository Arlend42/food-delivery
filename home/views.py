
from django.shortcuts import render
# from django.http import HttpResponse
from restaurants.models import Restaurant

# Create your views here.


def home(request):
    restaurants = Restaurant.objects.filter(is_approved=True, user__is_active=True)[:8]
    print(restaurants)
    context = {
        'restaurants': restaurants,
    }
    return render(request, "home.html", context)
