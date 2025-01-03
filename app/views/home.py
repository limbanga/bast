from django.shortcuts import render, redirect
from app.models import Product

PREFIX = "home"


def index(request):
    banner_images = [
        (
            "https://opencart4.magentech.com/themes/so_emarket/layout2/image/cache/catalog/slideshow/home2/slide-1-1920x620.jpg",
            "__carousel_item_1",
        ),
        (
            "https://opencart4.magentech.com/themes/so_emarket/layout2/image/cache/catalog/slideshow/home2/slide-2-1920x620.jpg",
            "__carousel_item_2",
        ),
        (
            "https://opencart4.magentech.com/themes/so_emarket/layout2/image/cache/catalog/slideshow/home2/slide-3-1920x620.jpg",
            "__carousel_item_3",
        ),
    ]

    tags = [
        {"name": "new", "label": "New arrivals"},
        {"name": "trend", "label": "Trending"},
        {"name": "onsale", "label": "Sales"},
    ]
    q = request.GET.get("q")
    if q:
        products = Product.objects.filter(name__icontains=q)
    else:
        products = Product.objects.all()
    valid_tags = [tag["name"] for tag in tags]  # Danh sách các tag hợp lệ
    selected_tag = request.GET.get("tag", "")  # Lấy tag từ query string
    # TODO: Xử lý lọc sản phẩm theo tag

    # Nếu tag không hợp lệ, gán giá trị mặc định hoặc chuyển hướng
    if selected_tag and selected_tag not in valid_tags:
        return redirect(f"{request.path}?tag=new")  # Chuyển hướng đến tag mặc định

    return render(
        request,
        f"{PREFIX}/index.html",
        {
            "banner_images": banner_images,
            "tags": tags,
            "products": products,
            "q": q,
            "selected_tag": selected_tag,
        },
    )


def product_detail(request, id):
    print("product_detail")
    product = Product.objects.get(id=id)
    return render(request, f"{PREFIX}/product_detail.html", {"product": product})
