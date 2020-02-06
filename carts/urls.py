from django.urls import path, include
from .views import cart_home

urlpatterns = [
    path('', cart_home, name='cart'),
]