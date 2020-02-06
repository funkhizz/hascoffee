from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, 'carts/home.html', {})

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print('product done')
            return redirect("carts:cart")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cart_obj.products.add(product_obj)
    return redirect("carts:cart")