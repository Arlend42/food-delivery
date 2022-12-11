from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Prefetch
from django.contrib.auth.decorators import login_required
from marketplace.context_processors import get_cart_counter
from restaurants.models import Restaurant
from menu.models import Category, Product
from .models import Cart

# Create your views here.


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def marketplace(request):
    restaurants = Restaurant.objects.filter(is_approved=True, user__is_active=True)
    restaurants_counter = restaurants.count()
    # print(restaurants)
    context = {
        "restaurants": restaurants,
        "restaurants_counter": restaurants_counter,
    }
    return render(request, "marketplace/restaurant_list.html", context)


def restaurant_detail(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, restaurant_slug=restaurant_slug)
    categories = Category.objects.filter(restaurant=restaurant).prefetch_related(
        Prefetch("products", queryset=Product.objects.filter(is_available=True))
    )  # categories that belong to this particular restaurant
    print(restaurant, categories)
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        "restaurant": restaurant,
        "categories": categories,
        "cart_items": cart_items,
    }
    return render(request, "marketplace/restaurant_detail.html", context)


def add_to_cart(request, product_id=None):
    if request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            try:
                # Check if the product exists
                product = Product.objects.get(id=product_id)
                # Check if the user has already added that food to the cart
                try:
                    check_cart = Cart.objects.get(user=request.user, product=product)
                    # Increase the cart quantity
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse(
                        {
                            "status": "Success",
                            "message": "Cart quantity icreased!",
                            "cart_counter": get_cart_counter(request),
                            "qty": check_cart.quantity,
                        }
                    )
                except:
                    check_cart = Cart.objects.create(
                        user=request.user, product=product, quantity=1
                    )
                    return JsonResponse(
                        {
                            "status": "Success",
                            "message": "Product has been added!",
                            "cart_counter": get_cart_counter(request),
                            "qty": check_cart.quantity,
                        }
                    )
            except:
                return JsonResponse(
                    {"status": "Failed", "message": "This product does not exist!"}
                )
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})
    else:
        return JsonResponse(
            {"status": "login_required!", "message": "Please login to continue!"}
        )


def remove_from_cart(request, product_id=None):
    if request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            try:
                # Check if the product exists
                product = Product.objects.get(id=product_id)
                # Check if the user has already added that food to the cart
                try:
                    check_cart = Cart.objects.get(user=request.user, product=product)
                    # Increase the cart quantity
                    if check_cart.quantity > 1:
                        check_cart.quantity -= 1
                        check_cart.save()
                    else:
                        check_cart.delete()
                        check_cart.quantity = 0
                    return JsonResponse(
                        {
                            "status": "Success",
                            "message": "Cart quantity decreased!",
                            "cart_counter": get_cart_counter(request),
                            "qty": check_cart.quantity,
                        }
                    )
                except:
                    return JsonResponse(
                        {
                            "status": "Failed",
                            "message": "This product is not in your cart!",
                        }
                    )
            except:
                return JsonResponse(
                    {"status": "Failed", "message": "This product does not exist!"}
                )
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})
    else:
        return JsonResponse(
            {"status": "login_required!", "message": "Please login to continue!"}
        )


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart_item(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse(
                        {
                            "status": "Success",
                            "message": "Cart item has been deleted!",
                            "cart_counter": get_cart_counter(request)
                        }
                    )
            except:
                return JsonResponse(
                    {"status": "Failed", "message": "Cart item does not exist!"}
                )
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})


def search(request):
    keyword = request.GET["keyword"]
    # get the restaurant ids that has the product user is searching for
    search_by_product = Product.objects.filter(
        food_name__icontains=keyword, is_available=True
    ).values_list("restaurant", flat=True)
    print(search_by_product)
    restaurants = Restaurant.objects.filter(
        Q(id__in=search_by_product)
        | Q(restaurant_name__icontains=keyword, is_approved=True, user__is_active=True)
    )
    # restaurants = Restaurant.objects.filter(restaurant_name__icontains=keyword, is_approved=True, user__is_active=True)
    restaurant_counter = restaurants.count()
    print(restaurants, restaurant_counter)
    context = {"restaurants": restaurants, "restaurant_counter": restaurant_counter}
    return render(request, "marketplace/restaurant_list.html", context)
