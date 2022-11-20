from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from restaurants.models import Restaurant
from menu.models import Category, Product
from django.db.models import Q

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


def search(request):
    keyword = request.GET['keyword']
    # get the restaurant ids that has the product user is searching for
    search_by_product = Product.objects.filter(food_name__icontains=keyword, is_available=True).values_list('restaurant', flat=True)
    print(search_by_product)
    restaurants = Restaurant.objects.filter(Q(id__in=search_by_product) | Q(restaurant_name__icontains=keyword, is_approved=True, user__is_active=True))
    # restaurants = Restaurant.objects.filter(restaurant_name__icontains=keyword, is_approved=True, user__is_active=True)
    restaurant_counter = restaurants.count()
    print(restaurants)
    context = {
        'restaurants': restaurants,
        'restaurant_counter': restaurant_counter
    }
    return render(request, 'marketplace/restaurant_list.html', context)