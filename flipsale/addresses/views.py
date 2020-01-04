from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .forms import AddressForm
from .models import Address
from billing.models import BillingProfile
from carts.models import Cart
from orders.models import Order
from django.views.generic import ListView

# Create your views here.
def create_address(request):
    next_post = request.POST.get('next_url')
    redirect_path = next_post or None
    addressForm = AddressForm(request.POST or None)
    if addressForm.is_valid():
        add_obj = addressForm.save(commit=False)
        add_obj.billing_profile = BillingProfile.objects.get_or_new(request)
        add_obj.save()
        attach_address(request, add_obj)
        if redirect_path:
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
    return redirect("home")

def attach_address(request, add_obj):
    cart_obj = Cart.objects.new_or_get(request)
    order_obj = Order.objects.get_or_new(cart_obj, add_obj.billing_profile)
    order_obj.address = add_obj
    order_obj.save()

def adding_selection(request):
    next_post = request.POST.get('next_url')
    redirect_path = next_post or None
    addid = request.POST.get("add_detail")
    add_obj = Address.objects.filter(id=addid).first()
    attach_address(request, add_obj)
    if redirect_path:
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect("home")

class AddressListView(ListView):
    template_name = "addresses/selectAddress.html"
    model = Address

    def get_context_data(self, *args, **kwargs):
        bill_obj = BillingProfile.objects.get_or_new(self.request)
        add_list = Address.objects.filter(billing_profile=bill_obj)
        return {'object_list' : add_list}
