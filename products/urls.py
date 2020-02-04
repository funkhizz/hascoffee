from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug>', views.product_detail, name='product_detail'),
    # path('<id>/', views.user_mail, name='user_email') emailing realtors
]