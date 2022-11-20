from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as marketplace_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('home.urls')),
    path("", include("accounts.urls")),
    path("marketplace/", include("marketplace.urls")),
    path('search/', marketplace_views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
