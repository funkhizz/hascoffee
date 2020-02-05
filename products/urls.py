from django.urls import path
from .views import product_detail, product_list

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<slug>', product_detail, name='product_detail'),
    # path('<id>/', views.user_mail, name='user_email') emailing realtors
]