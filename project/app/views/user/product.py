from django.shortcuts import render
from app.forms import ProductForm
PREFIX = 'user/products'

def index(request):
    return render(request, f'{PREFIX}/index.html')

def create(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save() # save the form to the database

    return render(request, f'{PREFIX}/edit.html', {'form': form})