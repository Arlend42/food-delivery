from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from menu.models import Category
from .forms import RestaurantForm
from .models import Restaurant


@login_required
def my_restaurant_profile(request):
    customer_profile = get_object_or_404(UserProfile, user=request.user)
    restaurant_profile = get_object_or_404(Restaurant, user=request.user)
    # to save changes in db
    if request.method == 'POST':
        customer_profile_form = UserProfileForm(request.POST, request.FILES, instance=customer_profile)
        restaurant_profile_form = RestaurantForm(request.POST, request.FILES, instance=restaurant_profile)
        if customer_profile_form.is_valid() and restaurant_profile_form.is_valid():
            customer_profile_form.save()
            restaurant_profile_form.save()
            messages.success(request, 'The restaurant info has been updated!')
            return redirect('my_restaurant_profile')
        else:
            print(customer_profile_form.errors)
            print(restaurant_profile_form.errors)
    else:   
        customer_profile_form = UserProfileForm(instance=customer_profile)
        restaurant_profile_form = RestaurantForm(instance=restaurant_profile)
    context = {
        'customer_profile_form': customer_profile_form,
        'restaurant_profile_form': restaurant_profile_form,
        'customer_profile': customer_profile,
        'restaurant_profile': restaurant_profile
    }
    return render(request, 'restaurants/my_restaurant_profile.html', context)


def menu_builder(request):
    restaurant = Restaurant.objects.get(user=request.user)
    categories = Category.objects.filter(restaurant=restaurant)
    context = {
        'categories': categories,
    }
    return render(request, 'restaurants/menu_builder.html', context)
