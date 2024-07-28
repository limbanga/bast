from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app.forms import CategoryForm

PREFIX = "user/categories"
INDEX_URL_NAME = "category_index"

def __get_analysis(category):
    return {
        "name": category.name,
        "product_count": category.product_set.count()
    }

def index(request):
    categories = request.user.category_set.all()
    
    analysis = map(__get_analysis, categories)

    test = list(analysis)
    return render(request, f"{PREFIX}/index.html", {"categories": categories, "test": test })


@login_required
def create(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():

            category = form.save(commit=False)  # commit=False means don't save yet
            category.owner = request.user
            category.save()
            return redirect(INDEX_URL_NAME)

    return render(request, f"{PREFIX}/edit.html", {"form": form})


@login_required
def edit(request, id):
    category = request.user.category_set.get(id=id)
    if not category:
        # TODO: return 404 later
        pass
    form = CategoryForm(instance=category)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect(INDEX_URL_NAME)
    return render(request, f"{PREFIX}/edit.html", {"form": form, "id": id})

@login_required
def confirm_delete(request, id):
    category = get_object_or_404(request.user.category_set, id=id)
    return render(request, f"{PREFIX}/confirm_delete.html", {"category": category})

@login_required
def delete(request, id):    
    category = get_object_or_404(request.user.category_set, id=id)
    category.delete()
    return redirect(INDEX_URL_NAME)