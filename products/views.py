from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Product
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .quantity_choices import quantity_choices, grind_choices
from carts.models import Cart

def product_detail(request, slug):
    instance = get_object_or_404(Product, slug=slug)
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    randomquery = [Product.objects.random() for i in range(6)]
    context = {
        'object_detail': instance,
        'quantity_choices': quantity_choices,
        'grind_choices': grind_choices,
        'random_products': randomquery,
        'cart': cart_obj
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

