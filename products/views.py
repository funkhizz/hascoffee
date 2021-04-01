from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Product
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .quantity_choices import quantity_choices, grind_choices
from carts.models import Cart
from itertools import chain


def product_detail(request, slug):
    instance = get_object_or_404(Product, slug=slug)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    print(Product.objects.all().count() + 1)
    qs_random = []

    while len(qs_random) < Product.objects.all().count() - 1:
        if len(qs_random) == 6:
            break
        else:
            randomquery = Product.objects.random()
            print(randomquery)
            if randomquery in qs_random or randomquery.title==instance.title:
                continue
            else:
                qs_random.append(randomquery)
    result_list = list(chain(qs_random))
    context = {
        'object_detail': instance,
        'quantity_choices': quantity_choices,
        'grind_choices': grind_choices,
        'random_products': result_list,
        'cart': cart_obj
    }
    return render(request, "product_detail.html", context)

def product_list(request):
    context = {}
    filter_params = request.POST.get('filter')
    if filter_params:
        if filter_params == 'all':
            products = Product.objects.order_by('-timestamp').filter(is_published=True)
            context = {
                'object_list': products
            }
            request.session['select_val'] = 'all'
        if filter_params == 'price-low':
            products = Product.objects.order_by('price').filter(is_published=True)
            context = {
                'object_list': products
            }
            request.session['select_val'] = 'price-low'

        if filter_params == 'price-high':
            products = Product.objects.order_by('-price').filter(is_published=True)
            context = {
                'object_list': products
            }
            request.session['select_val'] = 'price-high'

        if filter_params == 'date-old':
            products = Product.objects.order_by('timestamp').filter(is_published=True)
            context = {
                'object_list': products
            }
            request.session['select_val'] = 'date-old'

    else:
        try:
            del request.session['select_val']
        except:
            pass
        products = Product.objects.order_by('-timestamp').filter(is_published=True)
        paginator = Paginator(products, 10)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        context = {
            'object_list': paged_products,
        }
    return render(request, 'product_list.html', context)

