from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app.forms import ProductForm, ProductImageForm
from app.models import ProductImage, Product

from django.forms.models import inlineformset_factory


PREFIX = "user/products"
INDEX_URL_NAME = "product_index"

ProductImageFormSet = inlineformset_factory(
    Product, ProductImage, form=ProductImageForm, extra=4, max_num=4, can_delete=True
)


def index(request):
    products = request.user.product_set.all()
    return render(request, f"{PREFIX}/index.html", {"products": products})


@login_required
def create(request):
    form = ProductForm(request.user)
    formset = ProductImageFormSet()

    if request.method == "POST":
        form = ProductForm(request.user, request.POST or None)
        formset = ProductImageFormSet(request.POST or None, request.FILES)

        if form.is_valid() and formset.is_valid():
            product = form.save()

            for form_image in formset.cleaned_data:
                if form_image:
                    image = form_image["image"]
                    ProductImage.objects.create(product=product, image=image)

            return redirect(INDEX_URL_NAME)

    return render(request, f"{PREFIX}/edit.html", {"form": form, "formset": formset})


@login_required
def edit(request, id):
    product = get_object_or_404(request.user.product_set, id=id)
    form = ProductForm(request.user, instance=product)
    formset = ProductImageFormSet(instance=product)

    if request.method == "POST":
        form = ProductForm(request.user, request.POST or None, instance=product)
        formset = ProductImageFormSet(request.POST or None, request.FILES, instance=product)


        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect(INDEX_URL_NAME)
        else:
            print("form is invalid")
            # print("form.errors:", form.errors)
            print("formset.errors:", formset.errors[0])

    return render(request, f"{PREFIX}/edit.html", {"form": form, "formset": formset, 'id': id})



@login_required
def delete(request, id):    
    product = get_object_or_404(request.user.product_set, id=id)
    product.delete()
    return redirect(INDEX_URL_NAME)


def confirm_delete(request, id):
    product = request.user.product_set.get(id=id)
    if not product:
        pass
    return render(request, f"{PREFIX}/confirm_delete.html", {"product": product})
