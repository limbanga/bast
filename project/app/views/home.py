from django.shortcuts import render
from django.http import HttpResponseRedirect
from app.models import Product, OrderLine
from django.contrib.auth.decorators import login_required

PREFIX = "home"


def index(request):
    products = Product.objects.all()
    return render(request, f"{PREFIX}/index.html", {"products": products})


def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, f"{PREFIX}/product_detail.html", {"product": product})

@login_required
def add_to_cart(request, id):
    order_cart = request.user.orders.filter(status="cart").first()
    product = Product.objects.get(id=id)
    if not order_cart:
        order_cart = request.user.orders.create(status="cart")

    # Kiểm tra xem OrderLine đã tồn tại trong giỏ hàng chưa
    order_line, created = OrderLine.objects.get_or_create(
        product=product, defaults={"quantity": 1}
    )

    if not created:
        # Nếu OrderLine đã tồn tại, tăng số lượng
        order_line.quantity += 1
        order_line.save()
    order_cart.order_lines.add(order_line)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def checkout(request):
    order_cart = request.user.orders.filter(status="cart").first()
    if not order_cart:
        order_cart = request.user.orders.create(status="cart") 

    return render(
        request,
        f"{PREFIX}/checkout.html",
        {"order_cart": order_cart, "order_lines": order_cart.order_lines.all()},
    )
