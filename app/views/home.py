from django.shortcuts import render, redirect
from app.models import Product

PREFIX = "home"


def index(request):
    
    categories = [
        {
            "name": "Điện tử",
            "image": "https://doieur1arw9xr.cloudfront.net/optamark/images/product/TECHNOLOGY-PRODUCTS-ELECTRONICS.jpg",
            "url": "/categories/electronics/",
        },
        {
            "name": "Thời trang",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwA9V24GDNibnqXGVPXknlpgVZuGX9Fq__kw&s",
            "url": "/categories/fashion/",
        },
        {
            "name": "Làm vườn",
            "image": "https://www.rexlondon.com/sites/default/files/styles/square_800px/public/2022-01/29333_3-mini-garden-toolt-set-min.png?_buster=kWCJgQ17&itok=irfUUAlo",
            "url": "/categories/garden/",
        },
        {
            "name": "Thể thao",
            "image": "https://mybtoys.com/wp-content/uploads/BX2348_PR-1024x1024.png",
            "url": "/categories/sports/",
        },
        {
            "name": "Đồ gia dụng",
            "image": "https://www.acetestgroup.com/ck-images/Household%20Appliances_1739882319.png",
            "url": "/categories/home-appliances/",
        },
        {
            "name": "Đồ chơi trẻ em",
            "image": "https://cdn3d.iconscout.com/3d/premium/thumb/train-toys-3d-icon-download-in-png-blend-fbx-gltf-file-formats--transport-children-kids-pack-sports-games-icons-9436277.png?f=webp",
            "url": "/categories/toys/",
        },
        {
            "name": "Đồ nội thất",
            "image": "https://andersen-furniture.com/app/uploads/2025/01/2-90010_3-1.jpg",
            "url": "/categories/furniture/",
        },
        {
            "name": "Sách",
            "image": "https://hips.hearstapps.com/hmg-prod/images/bestbooks-1-6569d68fa426e.jpg?crop=0.502xw:1.00xh;0.247xw,0&resize=640:*",
            "url": "/categories/books/",
        },
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
            "categories": categories,
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
