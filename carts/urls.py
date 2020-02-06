from django.urls import path, include
from .views import cart_home, add_to_cart, remove_from_cart

app_name = 'carts'

urlpatterns = [
    path('', cart_home, name='cart'),
    path('add_cart/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),

]