from django.shortcuts import render, redirect
from django.contrib.auth.models import User

PREFIX = "user/shops/"


def index(request, id=None, username=None):
    if username:
        shop_owner = User.objects.filter(username=username)
    elif id:
        shop_owner = User.objects.get(id=id)
    elif request.user.is_authenticated:
        shop_owner = request.user
    else:
        return redirect("index")

    if not shop_owner:
        return redirect("index")

    products = shop_owner.product_set.all()
    categories = shop_owner.category_set.all()
    return render(
        request,
        f"{PREFIX}index.html",
        {"shop_owner": shop_owner, "products": products, "categories": categories},
    )


def dashboard(request):
    return render(request, f"{PREFIX}dashboard.html")
