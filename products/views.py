from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Product
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def product_detail(request, slug):
    instance = get_object_or_404(Product, slug=slug)
    context = {
        'object_detail': instance,
    }
    return render(request, "product_detail.html", context)

def product_list(request):
    products = Product.objects.order_by('-timestamp').filter(is_published=True)
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'object_list': paged_products,
    }
    return render(request, 'product_list.html', context)

