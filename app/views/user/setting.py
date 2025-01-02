from django.shortcuts import render
from django.contrib.auth.decorators import login_required

PREFIX = "user/setting"

@login_required
def index(request):
    return render(request, f"{PREFIX}/index.html")

