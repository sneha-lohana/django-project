from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from products.utils import unique_slug_generator

from products.models import Product
# from products.utils import unique_slug_generator

class Tag(models.Model):
    title       = models.CharField(max_length=120)
    slug = models.SlugField(null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=True)
    products    = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.title


def tag_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_slug_pre_save_receiver, sender=Tag)