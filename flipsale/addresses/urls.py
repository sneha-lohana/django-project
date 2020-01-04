from django.urls import path
from .views import create_address, adding_selection

urlpatterns = [
    path("create/", create_address, name="create"),
    path("attach/", adding_selection, name="attach")
]