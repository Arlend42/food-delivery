from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from accounts.forms import UserProfileForm, EditUserForm
# Create your views here.


@login_required(login_url='login')
def c_profile(request):
    customer_profile = get_object_or_404(UserProfile, user=request.user)  # logged in user information
    if request.method == 'POST':
        customer_profile_form = UserProfileForm(request.POST, request.FILES, instance=customer_profile)
        user_form = EditUserForm(request.POST, instance=request.user)
        if customer_profile_form.is_valid() and user_form.is_valid():
            customer_profile_form.save()
            user_form.save()
            messages.success(request, 'Profile uptaded successfully!')
            return redirect('c_profile')
        else:
            print(customer_profile_form.errors)
            print(user_form.errors)
    else:
        customer_profile_form = UserProfileForm(instance=customer_profile)
        user_form = EditUserForm(instance=request.user)
    context = {
        'customer_profile': customer_profile,
        'customer_profile_form': customer_profile_form,
        'user_form': user_form,
    }
    return render(request, 'customers/c_profile.html', context)
