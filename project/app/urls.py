from django.urls import path
from .views import home, auth, error_404_view
from .views.user import product, category, shop

urlpatterns = [
    # auth
    path('auth/login', auth.login, name='login'),
    path('auth/register', auth.register, name='register'),
    path('auth/logout', auth.logout, name='logout'),

    # home
    path('', home.index, name='index'),
    path('product/<int:id>', home.product_detail, name='home_product_detail'),
    path('add_to_cart/<int:id>', home.add_to_cart, name='add_to_cart'),
    path('checkout', home.checkout, name='checkout'),

    # user
    # user > products
    path('user/products', product.index, name='product_index'),
    path('user/products/create', product.create, name='product_create'),
    path('user/products/<int:id>/edit', product.edit, name='product_edit'),
    path('user/products/<int:id>/confirm_delete', product.confirm_delete, name='product_confirm_delete'),
    path('user/products/<int:id>/delete', product.delete, name='product_delete'),
    # user > categories
    path('user/categories', category.index, name='category_index'),
    path('user/categories/create', category.create, name='category_create'),
    path('user/categories/<int:id>/edit', category.edit, name='category_edit'),
    # user > shop
    path('user/shop/<int:id>', shop.index, name='shop'),
    path('user/shop/@<str:username>', shop.index, name='shop'),


    # admin


    #error

]

handler404 = error_404_view