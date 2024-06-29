from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.forms import ProductForm

PREFIX = "user/products"


def index(request):
    products = request.user.product_set.all()
    return render(request, f"{PREFIX}/index.html", {"products": products})


@login_required
def create(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():

            product = form.save(commit=False)  # commit=False means don't save yet
            product.owner = request.user
            product.save()
            return redirect("index")

    return render(request, f"{PREFIX}/edit.html", {"form": form})
