from django.urls import path
from .views import create_order, success

urlpatterns = [
    path("", create_order, name="create"),
    path("success", success, name="success"),
]