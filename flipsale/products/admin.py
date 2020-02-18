from django.contrib import admin
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product
    
    list_display = ['title', 'price', 'slug']
    search_fields = ['title', 'price', 'slug', 'description']

admin.site.register(Product, ProductAdmin)
