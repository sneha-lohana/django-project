from django.db import models
from django.urls import reverse
from django.db.models import Q

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    
    def search(self, query):
        lookups = (Q(title__icontains=query) | 
                  Q(description__icontains=query) |
                  Q(price__icontains=query) |
                  Q(tag__title__icontains=query))
        return self.filter(lookups).distinct()

# Create your models here.
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def search(self, query):
        return self.get_queryset().search(query)

class Product(models.Model):
    title = models.CharField(unique=True, max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=10)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)
    active = models.BooleanField(default=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    def __str__(self):
        return self.title
    
    def get_absoulte_url(self):
        return reverse("product:detail",kwargs={'pk':self.id})
