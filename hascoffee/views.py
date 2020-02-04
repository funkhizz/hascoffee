from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product

def home_page(request):
    new_in_queryset = Product.objects.order_by('-timestamp').filter(is_published=True)[:4]
    context = {'object_list': new_in_queryset,
    'new_object_list': '12345'}
    return render(request, 'homepage.html', context)

