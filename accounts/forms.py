from django import forms
from .models import User
from django.shortcuts import redirect


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "password",
        ]

        def clean(self):
            cleaned_data = super(UserForm, self).clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")
            if password != confirm_password:
                print(password, confirm_password)
                raise forms.ValidationError("Password must match!")
            return redirect("accounts/registerUser.html")
