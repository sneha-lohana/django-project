from django.shortcuts import render
from carts.models import Cart
from billing.models import BillingProfile
from .models import Order
from django.http import HttpResponse

# Create your views here.
def create_order(request):
    cart_obj = Cart.objects.new_or_get(request)
    if request.user.is_authenticated:
        bill_obj = BillingProfile.objects.get_or_new(request)
        order_obj = Order.objects.get_or_new(cart_obj, bill_obj)
    return HttpResponse(order_obj.order_id or None)
