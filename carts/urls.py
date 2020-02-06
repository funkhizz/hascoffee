from django.urls import path, include
from .views import cart_home, cart_update

app_name = 'carts'

urlpatterns = [
    path('', cart_home, name='cart'),
    path('update/', cart_update, name='cart_update'),

]