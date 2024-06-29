from django.shortcuts import render
from app.models import Product

PREFIX = 'home'

def index(request):
    products = Product.objects.all()
    return render(request, f'{PREFIX}/index.html', {'products': products})