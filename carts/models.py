from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import m2m_changed, pre_save, post_save
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = True
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        print(total)
        instance.total = total
        instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, validators=[MaxValueValidator(50), MinValueValidator(1)])
    line_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.title

# def cartitem_receiver(sender, instance, *args, **kwargs):
#     cartItem = CartItem.objects.filter(cart=instance.cart.id)
#     total = 0
#     for x in cartItem:
#         total += x.line_total

#     instance.cart.total = total
#     instance.cart.save()


# post_save.connect(cartitem_receiver, sender=CartItem)