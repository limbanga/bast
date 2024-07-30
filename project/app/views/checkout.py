from django.shortcuts import render
from django.http import HttpResponseRedirect
from app.models import Product, OrderLine, Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages

PREFIX = "checkout"

@login_required
def set_cart_item(request, id, quantity=1):
    # Get or create the cart of the user
    order_cart, _ = Order.objects.get_or_create(owner=request.user, status='cart')

    # Get the product or return 404
    product = get_object_or_404(Product, pk=id)

    order_line = order_cart.order_lines.filter(product=product).first()

    if quantity <= 0 and order_line:
        # If the quantity is less than or equal to 0, delete the order line
        order_line.delete()
        order_cart.order_lines.remove(order_line)
        messages.success(request, "Remove from cart successfully.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    if not order_line:
        order_line = OrderLine(product=product)

    order_line.quantity = quantity
    order_line.total = order_line.quantity * product.price
    order_line.save()

    # Update the total of the cart
    order_cart.order_lines.add(order_line)
    order_cart.total = sum([line.total for line in order_cart.order_lines.all()])
    order_cart.save()

    if quantity == 1:
        messages.success(request, "Add item to cart successfully")
    else:
        messages.success(request, "Update quantity successfully.")
    # Redirect back to the previous page
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def checkout(request):
    order_cart = request.user.orders.filter(status="cart").first()
    if not order_cart:
        order_cart = request.user.orders.create(status="cart") 

    return render(
        request,
        f"{PREFIX}/index.html",
        {"order_cart": order_cart,
        "order_lines": order_cart.order_lines.all()},
    )
