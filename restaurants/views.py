from django.shortcuts import render


def my_restaurant_profile(request):
    return render(request, 'restaurants/my_restaurant_profile.html')
