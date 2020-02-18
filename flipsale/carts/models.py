from django.db import models
# from django.contrib.auth.models import User
from products.models import Product
from django.db.models.signals import pre_save, post_save, m2m_changed
from decimal import Decimal

from django.contrib.auth import get_user_model
User = get_user_model()

class CartManager(models.Manager):
    def new_or_get(self, request):
        cartid = request.session.get('cartid' or None)
        if cartid:
            cart_obj = Cart.objects.filter(id=cartid, active=True).first()
        elif request.user.is_authenticated:
            cart_obj = Cart.objects.filter(user=request.user, active=True).first() or None
            if cart_obj is None:
                cart_obj = Cart.objects.create(user=request.user)
            request.session['cartid']=cart_obj.id
        else:
            cart_obj = Cart.objects.create()
            request.session['cartid']=cart_obj.id
        request.session['cart_count'] = cart_obj.products.all().count()
        return cart_obj

class Cart(models.Model):
    products = models.ManyToManyField(Product, blank=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    sub_total = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    createdDate = models.DateField(auto_now_add=True)
    updatedDate = models.DateField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

def m2m_changed_product_receiver(sender, instance, *args, **kwargs):
    # sub_total = 0
    if instance.products.all().count() > 0:
        instance.sub_total = 0
        for prod in instance.products.all():
            instance.sub_total += prod.price
        if instance.sub_total < Decimal(500):
            instance.total = instance.sub_total+Decimal(80)
        else:
            instance.total = instance.sub_total
        instance.save()

m2m_changed.connect(m2m_changed_product_receiver, sender=Cart.products.through)