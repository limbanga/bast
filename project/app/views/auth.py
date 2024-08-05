from django.shortcuts import render, redirect
from django.contrib.auth import login as _login, logout as _logout
from app.forms import AppAuthenticationForm, AppUserCreationForm
from app.models import UserInformation

PREFIX = "auth"

def login(request):
    form = AppAuthenticationForm()
    if request.method == "POST":
        form = AppAuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            user = form.get_user()
            _login(request, user)
            return redirect("index")  # redirect to the home page
    return render(request, f"{PREFIX}/login.html", {"form": form})

def register(request):
    form = AppUserCreationForm()
    if request.method == "POST":
        form = AppUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # TODO: test
            user_information = UserInformation(user=user)
            user_information.save()
            # log the user in
            _login(request, user)
            return redirect("index")  # redirect to the home page
    return render(request, f"{PREFIX}/register.html", {"form": form})

def logout(request):
    _logout(request)
    return redirect("login")  # redirect to the home page
