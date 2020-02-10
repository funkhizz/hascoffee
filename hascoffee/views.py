from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product

def home_page(request):
    new_in_queryset = Product.objects.order_by('-timestamp').filter(is_published=True)[:4]
    best_sellers = Product.objects.order_by('-item_sold').filter(is_published=True)[:5]
    context = {'object_list': new_in_queryset,
    'new_object_list': best_sellers}
    return render(request, 'homepage.html', context)

