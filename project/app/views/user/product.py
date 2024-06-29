from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.forms import ProductForm

PREFIX = "user/products"
INDEX_URL_NAME = "product_index"


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
            return redirect(INDEX_URL_NAME)

    return render(request, f"{PREFIX}/edit.html", {"form": form})


@login_required
def edit(request, id):
    product = request.user.product_set.get(id=id)
    if not product:
        # TODO: return 404 later
        pass
    form = ProductForm(instance=product)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect(INDEX_URL_NAME)
    return render(request, f"{PREFIX}/edit.html", {"form": form, "id": id})


@login_required
def delete(request, id):
    product = request.user.product_set.get(id=id)
    if not product:
        # TODO: Return 404 later
        return redirect(INDEX_URL_NAME)
    product.delete()
    return redirect(INDEX_URL_NAME)

def confirm_delete(request, id):
    product = request.user.product_set.get(id=id)
    if not product:
        pass
    return render(request, f"{PREFIX}/confirm_delete.html", {"product": product})
