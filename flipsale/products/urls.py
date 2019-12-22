from django.urls import path
from .views import get_product_list, ProductListView, ProductDetailView

urlpatterns = [
    path("fbv/", get_product_list, name="fbv"),
    path("cbv/", ProductListView.as_view(), name="cbv"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail")
]