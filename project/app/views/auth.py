from django.shortcuts import render, redirect
from django.contrib.auth import login as _login, logout as _logout
from django.contrib import messages
from app.forms import AppAuthenticationForm, AppUserCreationForm, AppChangePasswordForm
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


def change_password(request):
    form = AppChangePasswordForm(user=request.user)
    if request.method == "POST":
        form = AppChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully.")

            return redirect("login")  # redirect to the login page
        else:
            print(form.errors)
    return render(request, f"{PREFIX}/change_password.html", {"form": form})

def reset_password(request):
    #  TODO: implement reset password
    return render(request, f"{PREFIX}/reset_password.html")