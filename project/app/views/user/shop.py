from django.shortcuts import render

PREFIX = "user/shops/"

def index(request, id=None, username=None):
    if username:
        return render(request, f"{PREFIX}index.html", {"username": username})

    return render(request, f"{PREFIX}index.html", {"id": id})