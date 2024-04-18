from django.urls import path
from products.views import *

urlpatterns = [
    path("<slug>/", get_product, name="get_product"),
    path("product/search/", search_view, name="product_search"),
]