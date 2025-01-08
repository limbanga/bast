from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from app.forms import UserForm, UserInformationForm, AddressForm
from app.models import UserInformation

PREFIX = "user/shops/"


def index(request, id=None, username=None):
    if username:
        shop_owner = User.objects.get(username=username)
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

    q = request.GET.get("q", "")
    if q:
        products = products.filter(name__icontains=q)

    queryCategory = request.GET.get("cate", "")
    if queryCategory:
        products = products.filter(category__slug=queryCategory)

    return render(
        request,
        f"{PREFIX}index.html",
        {
            "shop_owner": shop_owner,
            "products": products,
            "categories": categories,
            "q": q,
            "queryCategory": queryCategory,
        },
    )


def dashboard(request):
    return render(request, f"{PREFIX}dashboard.html")


def edit(request):

    form = UserForm(instance=request.user)
    # Kiểm tra và tạo hoặc lấy UserInformation cho user hiện tại
    user_information, created = UserInformation.objects.get_or_create(user=request.user)

    informationForm = UserInformationForm(instance=user_information)

    addressForm = AddressForm(instance=request.user)

    if request.method == "POST":
        print(f"user: {request.user}")
        print(f"post: {request.POST}")
        form = UserForm(request.POST, instance=request.user)
        informationForm = UserInformationForm(
            request.POST, request.FILES, instance=request.user.information
        )
        if informationForm.is_valid() and form.is_valid():
            print(f"form: {form.cleaned_data}")
            form.save()
            informationForm.save()
            messages.success(request, "Information updated")
            return redirect("shop")
        else:
            messages.error(request, "Error updating information")
            print(f"form errors: {form.errors}")
            print(f"informationForm errors: {informationForm.errors}")
    return render(
        request,
        f"{PREFIX}edit.html",
        {"form": form, "informationForm": informationForm, "addressForm": addressForm},
    )
