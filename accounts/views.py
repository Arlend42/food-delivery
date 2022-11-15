from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .forms import UserForm
from .models import User, UserProfile
from restaurants.forms import RestaurantForm
from .utils import determine_user, verification_email


def register_user(request):
    if request.user.is_authenticated:
        return redirect('my_account')
    elif request.method == "POST":
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                phone_number=phone_number,
                password=password,
            )
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Please check the email for the confirmation link!')
            # verification email
            mail_subject = 'Please activate yout account'
            email_template = 'accounts/emails/account_verification_email.html'
            verification_email(request, user, mail_subject, email_template)
            return redirect("register_user")
        else:
            print("Invalid Form")
            print(form.errors)
    else:
        form = UserForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/registerUser.html", context)


def register_restaurants(request):
    if request.user.is_authenticated:
        return redirect('my_account')
    elif request.method == "POST":
        form = UserForm(request.POST)
        restaurant_form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid() and restaurant_form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                phone_number=phone_number,
                password=password,
            )
            user.role = User.RESTAURANT
            user.save()
            restaurant = restaurant_form.save(commit=False)
            restaurant.user = user
            user_profile = UserProfile.objects.get(user=user)
            restaurant.user_profile = user_profile
            restaurant.save()
            print(user)
            mail_subject = 'Please activate yout account'
            email_template = 'accounts/emails/account_verification_email.html'
            messages.success(request, 'Thank you! Will come back to you ASAP')
            verification_email(request, user, mail_subject, email_template)
            return redirect('register_restaurants')
        else:
            print("Invalid Form")
            print(form.errors)
    else:
        form = UserForm()
        restaurant_form = RestaurantForm()
    context = {
        "form": form,
        "restaurant_form": restaurant_form,
    }
    return render(request, "accounts/registerRestaurant.html", context)


def activate_account(request, uidb64, token):
    # activate user by setting is_active status to true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user is None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is activated!')
        return redirect('my_account')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('my_account')


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('my_account')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)  
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('my_account')
        else:
            messages.error(request, 'Invalid email or password!')
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out!')
    return redirect('login')


@login_required(login_url='login')
def my_account(request):
    user = request.user
    redirectUrl = determine_user(user)
    return redirect(redirectUrl)


@login_required(login_url='login')
def customer_profile(request):
    return render(request, 'accounts/customer_profile.html')


@login_required(login_url='login')
def restaurant_profile(request):
    return render(request, 'accounts/restaurant_profile.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            # send reset password email
            mail_subject = 'Reset Password'
            email_template = 'accounts/emails/reset_password_email.html'
            verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Password reset link has been sent to your email!')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # Validate the user by decoding the token and userpk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user is None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password!')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('my_account')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Password did not match!')
            return redirect('reset_password')

    return render(request, 'accounts/reset_password.html')
