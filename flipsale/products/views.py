from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product
from carts.models import Cart

def get_product_list(request):
    prod_list = Product.objects.all()
    context = {'object_list': prod_list}
    return render(request, "products/list.html", context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        cart_obj = Cart.objects.new_or_get(self.request)
        context['in_cart'] = context['object'] in cart_obj.products.all()
        return context

class ProductListView(ListView):
    model = Product
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     prod_list = Product.objects.all()
    #     context = {'object_list': prod_list}
    #     return context

# Create your views here.
# 1. class based views
# 2. function based view

# Generic view List  View