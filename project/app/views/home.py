from django.shortcuts import render
from app.models import Product

PREFIX = 'home'

def index(request):
    products = Product.objects.all()
    return render(request, f'{PREFIX}/index.html', {'products': products})


def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, f'{PREFIX}/product_detail.html', {'product': product})