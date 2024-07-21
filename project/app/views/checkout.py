from django.shortcuts import render
from django.http import HttpResponseRedirect
from app.models import Product, OrderLine, Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

PREFIX = "checkout"

@login_required
def set_cart_item(request, id, quantity=1):
    # Get or create the cart of the user
    order_cart, created = Order.objects.get_or_create(owner=request.user, status='cart')

    # Get the product or return 404
    product = get_object_or_404(Product, pk=id)

    order_line = order_cart.order_lines.filter(product=product).first()

    if not order_line:
      order_line = OrderLine(product=product)

    order_line.quantity = quantity
    order_line.total = order_line.quantity * product.price
    order_line.save()

    if order_line.quantity <= 0:
        # If quantity is less than or equal to 0, remove from cart
        order_line.delete()

    # Update the total of the cart
    order_cart.order_lines.add(order_line)
    order_cart.total = sum([line.total for line in order_cart.order_lines.all()])
    order_cart.save()

    # Redirect back to the previous page
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def checkout(request):
    print('checkout')
    order_cart = request.user.orders.filter(status="cart").first()
    if not order_cart:
        order_cart = request.user.orders.create(status="cart") 

    print(order_cart)
    print(order_cart.total)
    print(order_cart.order_lines.all())


    return render(
        request,
        f"{PREFIX}/index.html",
        {"order_cart": order_cart,
        "order_lines": order_cart.order_lines.all()},
    )
