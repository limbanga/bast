from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, auth, checkout, error_404_view
from .views.user import product, category, shop, profile

urlpatterns = [
    # auth
    path('auth/login', auth.login, name='login'),
    path('auth/register', auth.register, name='register'),
    path('auth/logout', auth.logout, name='logout'),
    path('auth/change_password', auth.change_password, name='change_password'),
    path('auth/reset_password', auth.reset_password , name='reset_password'),

    # home
    path('', home.index, name='index'),
    path('product/<int:id>', home.product_detail, name='home_product_detail'),
    # cart
    path('set_cart_item/<int:id>/<int:quantity>', checkout.set_cart_item, name='set_cart_item'),
    path('checkout', checkout.checkout, name='checkout'),

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
    path('user/categories/<int:id>/confirm_delete', category.confirm_delete, name='category_confirm_delete'),
    path('user/categories/<int:id>/delete', category.delete, name='category_delete'),

    # user > shop
    path('user/shop', shop.index, name='shop'),
    path('user/shop/<int:id>', shop.index, name='shop'),
    path('user/shop/@<str:username>', shop.index, name='shop'),
    path('user/shop/edit', shop.edit, name='shop_edit'),
    # user > dashboard
    path('user/dashboard', shop.dashboard, name='dashboard'),
    # user > profile
    path('user/profile', profile.index, name='profile'),

    # admin


    #error

]

handler404 = error_404_view
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)