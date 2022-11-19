from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from restaurants.models import Restaurant
from menu.models import Category, Product

# Create your views here.


def marketplace(request):
    restaurants = Restaurant.objects.filter(is_approved=True, user__is_active=True)
    restaurants_counter = restaurants.count()
    # print(restaurants)
    context = {
        'restaurants': restaurants,
        'restaurants_counter': restaurants_counter,
    }
    return render(request, 'marketplace/restaurant_list.html', context)


def restaurant_detail(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, restaurant_slug=restaurant_slug)
    categories = Category.objects.filter(restaurant=restaurant).prefetch_related(
        Prefetch(
            'products',
            queryset=Product.objects.filter(is_available=True)
        )
    )  # categories that belong to this particular restaurant
    print(restaurant, categories)
    context = {
        'restaurant': restaurant,
        'categories': categories,
    }
    return render(request, 'marketplace/restaurant_detail.html', context)
