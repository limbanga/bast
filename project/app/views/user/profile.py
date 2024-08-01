from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

PREFIX = "user/profile"

@login_required
def index(request):
    products = request.user.product_set.all()
    return render(request, f"{PREFIX}/index.html", {"products": products})

