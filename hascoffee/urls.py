from django.contrib import admin
from django.urls import path, include
from .views import home_page
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', home_page, name='home'),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('carts.urls', namespace='carts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
