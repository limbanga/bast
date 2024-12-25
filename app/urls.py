from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, checkout, auth, error_404_view
from .views.user import product, category, shop, profile

auth_urls = ([
    path("comple_account_infomation", auth.comple_account_infomation, name="comple_account_infomation"),
    path("verify_email", auth.verify_email, name="verify_email"),
    path("reset_password_email_sent", auth.reset_password_email_sent, name="reset_password_email_sent"),
    path("reset_password/<str:token>/<str:uidb64>", auth.process_reset_password, name="process_reset_password"),
], "auth")

urlpatterns = [
    # auth
    path("auth/", include(auth_urls)),
    # home
    path("", home.index, name="index"),
    path("product/<int:id>", home.product_detail, name="home_product_detail"),
    # cart
    path(
        "set_cart_item/<int:id>/<int:quantity>",
        checkout.set_cart_item,
        name="set_cart_item",
    ),
    path("checkout", checkout.checkout, name="checkout"),
    # user
    # user > products
    path("user/products", product.index, name="product_index"),
    path("user/products/create", product.create, name="product_create"),
    path("user/products/<int:id>/edit", product.edit, name="product_edit"),
    path(
        "user/products/<int:id>/confirm_delete",
        product.confirm_delete,
        name="product_confirm_delete",
    ),
    path("user/products/<int:id>/delete", product.delete, name="product_delete"),
    # user > categories
    path("user/categories", category.index, name="category_index"),
    path("user/categories/create", category.create, name="category_create"),
    path("user/categories/<int:id>/edit", category.edit, name="category_edit"),
    path(
        "user/categories/<int:id>/confirm_delete",
        category.confirm_delete,
        name="category_confirm_delete",
    ),
    path("user/categories/<int:id>/delete", category.delete, name="category_delete"),
    # user > shop
    path("user/shop", shop.index, name="shop"),
    path("user/shop/<int:id>", shop.index, name="shop"),
    path("user/shop/@<str:username>", shop.index, name="shop"),
    path("user/shop/edit", shop.edit, name="shop_edit"),
    # user > dashboard
    path("user/dashboard", shop.dashboard, name="dashboard"),
    # user > profile
    path("user/profile", profile.index, name="profile"),
    # admin
    # error
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = error_404_view
