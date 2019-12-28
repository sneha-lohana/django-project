from django.urls import path
from .views import create_order

urlpatterns = [
    path("", create_order, name="create"),
]