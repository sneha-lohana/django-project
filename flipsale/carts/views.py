from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product

def cart_home(request):
    cart_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/list.html", {'cart_obj':cart_obj})

def update_cart(request):
    if request.method == 'POST':
        prodid = request.POST.get('prodid')
        prod_obj = Product.objects.filter(id=prodid).first()
        print(prod_obj)
        cart_obj = Cart.objects.new_or_get(request)
        if prod_obj in cart_obj.products.all():
            cart_obj.products.remove(prod_obj)
        else:
            cart_obj.products.add(prod_obj)
    return redirect("cart:list")