from django.shortcuts import render, redirect
from .models import Cart, CartItem
from products.models import Product
from decimal import Decimal
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from orders.models import Order
from billing.models import BillingProfile
from accounts.models import GuestEmail
from django.contrib import messages

User = get_user_model()

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
        cart_quantity = 0
        all_items = CartItem.objects.filter(cart=cart_obj)
        for item in all_items:
            cart_quantity += item.quantity
        request.session["cart_items"] = cart_quantity
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
            cart_items = request.session.get("cart_items")
            cart_items -= cartitem.quantity
            request.session['cart_items'] = cart_items


        else:
            if cart_item.quantity > 1:
                cart_item.quantity -= int(quantity)
                line_total = product_obj.price * cart_item.quantity
                cart_item.line_total = line_total
                cart_obj.total -= product_obj.price * int(quantity)
                cart_item.save()
                cart_obj.save()
                cart_items = request.session.get("cart_items")
                cart_items -= 1
                request.session['cart_items'] = cart_items
            else:
                cartitem = CartItem.objects.get(id=cart_item.id)
                cartitem.cart = None
                cart_obj.total -= product_obj.price * int(quantity)
                cart_obj.save()
                cartitem.save()
                cart_items = request.session.get("cart_items")
                cart_items -= 1
                request.session['cart_items'] = cart_items
    return redirect("carts:cart")

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created and CartItem.objects.filter(cart=cart_obj.id).count() == 0:
        return redirect("carts:cart")
    cartItems = CartItem.objects.filter(cart=cart_obj.id)
    context = {
        'cart_items': cartItems,
        'cart': cart_obj,
        'order': order_obj,
    }
    return render(request, 'checkout.html', context)

def checkout_shipping(request):
    order_obj = None
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    email = request.POST.get('email')
    request.session['email_id'] = email
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    if billing_profile is not None:
        order_obj , order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    cartItems = CartItem.objects.filter(cart=cart_obj.id)

    context = {
        'billing_profile': billing_profile,
        'object': order_obj,
        'cart_items': cartItems
    }
    return render(request, 'checkout_shipping.html', context)
