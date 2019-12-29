from django.urls import path
from .views import create_address

urlpatterns = [
    path("create/", create_address, name="create")
]