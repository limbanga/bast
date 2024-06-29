from django.urls import path
from .views import home, auth, error_404_view
from .views.user import product

urlpatterns = [
    # auth
    path('auth/login', auth.login, name='login'),
    path('auth/register', auth.register, name='register'),
    path('auth/logout', auth.logout, name='logout'),

    # home
    path('', home.index, name='index'),

    # user
    # user > products
    path('user/products', product.index, name='product_index'),
    path('user/products/create', product.create, name='product_create'),
    path('user/products/<int:id>/edit', product.edit, name='product_edit'),
    path('user/products/<int:id>/delete', product.delete, name='product_delete'),
    # admin


    #error

]

handler404 = error_404_view