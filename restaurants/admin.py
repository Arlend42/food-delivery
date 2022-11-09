from django.contrib import admin
from restaurants.models import Restaurant


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("user", "restaurant_name", "is_approved", "create_at", "modified_at")
    list_display_links = ('user', 'restaurant_name',)


admin.site.register(Restaurant, RestaurantAdmin)
