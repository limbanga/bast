from django.shortcuts import render, redirect
from django.contrib.auth.models import User

PREFIX = "user/shops/"


def index(request, id=None, username=None):
    if username:
        shop_owner = User.objects.get(username=username)
    elif id:
        shop_owner = User.objects.get(id=id)
    else:
        # TODO: redirect to 404, show error message
        return redirect("index")
    products = shop_owner.product_set.all()

    return render(request, f"{PREFIX}index.html", {"shop_owner": shop_owner, "products": products})


def dashboard(request):
    return render(request, f"{PREFIX}dashboard.html")