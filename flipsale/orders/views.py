from django.shortcuts import render
from carts.models import Cart
from billing.models import BillingProfile
from .models import Order
from django.http import HttpResponse
from accounts.forms import LoginForm
from addresses.forms import AddressForm

# Create your views here.
def create_order(request):
    loginform = LoginForm()
    address = AddressForm()
    context = {'loginform':loginform, 'address':address}
    cart_obj = Cart.objects.new_or_get(request)
    if request.user.is_authenticated:
        bill_obj = BillingProfile.objects.get_or_new(request)
        order_obj = Order.objects.get_or_new(cart_obj, bill_obj)
        context["ord_obj"]=order_obj
    # return HttpResponse(order_obj.order_id or None)
    return render(request, "orders/placeorder.html", context)
