from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from menu.models import Category, Product
from menu.forms import CategoryForm, ProductForm
from .forms import RestaurantForm
from .models import Restaurant


@login_required(login_url='login')
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
        'restaurant_profile': restaurant_profile,
    }
    return render(request, 'restaurants/my_restaurant_profile.html', context)


@login_required(login_url='login')
def menu_builder(request):
    restaurant = Restaurant.objects.get(user=request.user)
    categories = Category.objects.filter(restaurant=restaurant).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'restaurants/menu_builder.html', context)


@login_required(login_url='login')
def products_by_category(request, pk=None):
    restaurant = Restaurant.objects.get(user=request.user)
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(restaurant=restaurant, category=category)
    print(products)
    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'restaurants/products_by_category.html', context)


@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.restaurant = Restaurant.objects.get(user=request.user)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context = {
        'form': form
    }
    return render(request, 'restaurants/add_category.html', context)


@login_required(login_url='login')
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.restaurant = Restaurant.objects.get(user=request.user)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'restaurants/edit_category.html', context)


@login_required(login_url='login')
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully')
    return redirect('menu_builder')


@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            food_name = form.cleaned_data['food_name']
            product = form.save(commit=False)
            product.restaurant = Restaurant.objects.get(user=request.user)
            product.slug = slugify(food_name)
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('products_by_category', product.category.id)
        else:
            print(form.errors)
    else:
        form = ProductForm()
        # Modify the form
        form.fields['category'].queryset = Category.objects.filter(restaurant=Restaurant.objects.get(user=request.user))
    context = {
        'form': form,
    }
    return render(request, 'restaurants/add_product.html', context)


@login_required(login_url='login')
def edit_product(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            food_name = form.cleaned_data['food_name']
            product = form.save(commit=False)
            product.restaurant = Restaurant.objects.get(user=request.user)
            product.slug = slugify(food_name)
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('products_by_category', product.category.id)
        else:
            print(form.errors)
    else:
        form = ProductForm(instance=product)
        form.fields['category'].queryset = Category.objects.filter(restaurant=Restaurant.objects.get(user=request.user))
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'restaurants/edit_product.html', context)


@login_required(login_url='login')
def delete_product(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product has been deleted successfully')
    return redirect('products_by_category', product.category.id)
