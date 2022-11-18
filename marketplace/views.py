from django.shortcuts import render
from restaurants.models import Restaurant


def marketplace(request):
    restaurants = Restaurant.objects.filter(is_approved=True, user__is_active=True)
    restaurants_counter = restaurants.count()
    print(restaurants)
    context = {
        'restaurants': restaurants,
        'restaurants_counter': restaurants_counter,
    }
    return render(request, 'marketplace/restaurant_list.html', context)
