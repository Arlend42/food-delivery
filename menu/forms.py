from django import forms
from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']


class ProductForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}))

    class Meta:
        model = Product
        fields = ['category', 'food_name', 'description', 'price', 'image', 'is_available']
