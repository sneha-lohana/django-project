from django.db import models
from billing.models import BillingProfile
from carts.models import Cart
from django.db.models.signals import pre_save
from products.utils import unique_orderid_generator

ORDER_STATUS_CHOICES = (
    # ('stored in db', 'view of form')
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('refunded', 'Refunded'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled')
)
class OrderManager(models.Manager):
    def get_or_new(self, cart_obj, bill_obj):
        order_obj = self.get_queryset().filter(cart=cart_obj, billingProfile=bill_obj, status='created').first() or None
        if order_obj is None:
            order_obj = self.get_queryset().create(cart=cart_obj, billingProfile=bill_obj)
        return order_obj

# Create your models here.
class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True, unique=True) #ASFGHH3345678SDFGHJK
    billingProfile = models.ForeignKey(BillingProfile, on_delete=models.PROTECT)
    # address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, default='created', choices=ORDER_STATUS_CHOICES)
    order_total = models.DecimalField(max_digits=8, decimal_places=2, default=0.0) #cart total
    total = models.DecimalField(max_digits=8, decimal_places=2,default=0.0)  # order_total + 18 % GST

    objects = OrderManager()

    def __str__(self):
        return self.order_id

def order_orderid_pre_save_receiver(sender, instance, *args,**kwargs):
    if instance.order_id == "" or instance.order_id is None:
        instance.order_id = unique_orderid_generator(instance)

pre_save.connect(order_orderid_pre_save_receiver, sender=Order)