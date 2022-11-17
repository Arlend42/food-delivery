from django.contrib import admin
from .models import Category, Product

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'restaurant', 'updated_at',)
    search_fields = ('category_name', 'restaurant__restaurant_name')


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_name',)}
    list_display = ('food_name', 'category', 'restaurant', 'price', 'is_available', 'updated_at',)
    search_fields = ('food_name', 'category__category_name', 'restaurant__restaurant_name',)
    list_filter = ('is_available',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
