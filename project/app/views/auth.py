from django.shortcuts import render, redirect
from django.contrib.auth import login as _login, logout as _logout
from django.contrib import messages
from app.forms import AppAuthenticationForm, AppUserCreationForm, AppChangePasswordForm, ResetPasswordForm
from app.models import UserInformation
from django.contrib.auth.models import User

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
    form = ResetPasswordForm()
    if request.method == "POST":
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            try:
                user = User.objects.get(email=form.cleaned_data["email"])
                # send email
                messages.success(request, "Email sent.")
                # TODO: send email
                # redirect to the OTP page
                return redirect("reset_password_email_sent")
            except User.DoesNotExist:
                messages.error(request, "User not found.")
                form.add_error(None, "User not found.")

        else:
            print(form.errors)

    return render(request, f"{PREFIX}/reset_password.html", {"form": form})

def reset_password_email_sent(request):
    return render(request, f"{PREFIX}/reset_password_email_sent.html")