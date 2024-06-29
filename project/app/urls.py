from django.urls import path
from .views import home, auth
from .views.user import product

urlpatterns = [
    # auth
    path('auth/login', auth.login, name='login'),
    path('auth/register', auth.register, name='register'),
    path('auth/logout', auth.logout, name='logout'),

    # home
    path('', home.index, name='index'),

    # user
    path('user/product/create', product.create, name='product_create'),

    # admin


]
