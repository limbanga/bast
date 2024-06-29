from django.urls import path
from .views import home
from .views.user import product

urlpatterns = [
    path('', home.index, name='index'),

    # user
    path('user/product/create', product.create, name='product_create'),
]
