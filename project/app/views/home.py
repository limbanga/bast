from django.shortcuts import render

PREFIX = 'home'

def index(request):
    return render(request, f'{PREFIX}/index.html')