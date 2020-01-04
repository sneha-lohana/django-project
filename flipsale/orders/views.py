from django.shortcuts import render
from carts.models import Cart
from billing.models import BillingProfile
from .models import Order
from django.http import HttpResponse
from accounts.forms import LoginForm
from addresses.forms import AddressForm
from addresses.models import Address

# Create your views here.
def create_order(request):
    loginform = LoginForm()
    address = AddressForm()
    context = {'loginform':loginform, 'address':address}
    cart_obj = Cart.objects.new_or_get(request)
    if request.user.is_authenticated:
        bill_obj = BillingProfile.objects.get_or_new(request)
        print(bill_obj)
        order_obj = Order.objects.get_or_new(cart_obj, bill_obj)
        add_list = Address.objects.filter(billing_profile=bill_obj)
        context["ord_obj"]=order_obj
        if add_list.count() > 0:
            context["add_list"]=add_list
    # return HttpResponse(order_obj.order_id or None)
    return render(request, "orders/placeorder.html", context)
