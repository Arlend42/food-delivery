from django import forms
from .models import Restaurant


class RestaurantForm(forms.ModelForm):
    nipt = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))

    class Meta:
        model = Restaurant
        fields = [
            "restaurant_name",
            "nipt",
        ]
