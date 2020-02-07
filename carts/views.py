from django.shortcuts import render, redirect
from .models import Cart, CartItem
from products.models import Product
from decimal import Decimal

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cartItems = CartItem.objects.filter(cart=cart_obj.id)
    context = {
        'cart_items': cartItems,
        'cart': cart_obj
    }
    return render(request, 'cart_home.html', context)

def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("carts:cart")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart_obj, product=product_obj)
        cart_item.quantity += int(quantity)
        line_total = product_obj.price * cart_item.quantity
        cart_item.line_total = line_total
        cart_obj.total += product_obj.price * int(quantity)
        cart_item.save()
        cart_obj.save()
    return redirect("carts:cart")

def remove_from_cart(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("carts:cart")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart_obj, product=product_obj)
        if int(quantity) == 0:
            cartitem = CartItem.objects.get(id=cart_item.id)
            cart_obj.total -= cartitem.line_total
            cartitem.cart = None
            cartitem.save()
            cart_obj.save()
        else:
            if cart_item.quantity > 1:
                cart_item.quantity -= int(quantity)
                line_total = product_obj.price * cart_item.quantity
                cart_item.line_total = line_total
                cart_obj.total -= product_obj.price * int(quantity)
                cart_item.save()
                cart_obj.save()
            else:
                cartitem = CartItem.objects.get(id=cart_item.id)
                cartitem.cart = None
                cart_obj.total -= product_obj.price * int(quantity)
                cart_obj.save()
                cartitem.save()
    return redirect("carts:cart")

def checkout_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cartItems = CartItem.objects.filter(cart=cart_obj.id)
    context = {
        'cart_items': cartItems,
        'cart': cart_obj

    }
    return render(request, 'checkout.html', context)
