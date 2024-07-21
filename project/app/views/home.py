from django.shortcuts import render
from app.models import Product

PREFIX = "home"


def index(request):
    q = request.GET.get("q")
    if q:
        products = Product.objects.filter(name__icontains=q)
    else:
        products = Product.objects.all()
    return render(request, f"{PREFIX}/index.html", {"products": products, "q": q })


def product_detail(request, id):
    print('product_detail')
    product = Product.objects.get(id=id)
    return render(request, f"{PREFIX}/product_detail.html", {"product": product})

