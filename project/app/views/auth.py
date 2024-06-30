from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login as _login, logout as _logout
PREFIX = "auth"

def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            user = form.get_user()
            _login(request, user)
            return redirect("index")  # redirect to the home page
    return render(request, f"{PREFIX}/login.html", {"form": form})

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in
            _login(request, user)
            return redirect("index")  # redirect to the home page
    return render(request, f"{PREFIX}/register.html", {"form": form})

def logout(request):
    _logout(request)
    return redirect("login")  # redirect to the home page