# from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
# Create your views here.


def registerUser(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                 first_name=first_name, last_name=last_name, email=email,
                 username=username, phone_number=phone_number, password=password)
            user.role = User.CUSTOMER
            user.save()
            print('this user is created')
            return redirect('registerUser')
        else:
            print('Invalid Form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
         'form': form,
     }
    return render(request, 'accounts/registerUser.html', context)
