from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as _login, logout as _logout
from django.contrib import messages
from app.forms import (
    AppAuthenticationForm,
    AppChangePasswordForm,
    ResetPasswordForm,
    UserForm,
)
from app.models import UserInformation
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode
from app.utils import generate_random_password

PREFIX = "auth"

@login_required
def comple_account_infomation(request):
    # Check if user has email
    if request.user.email:
        messages.warning(request, "Your account information already completed.")
        return redirect("index")

    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)

        is_valid = form.is_valid()
        if User.objects.filter(email=form.cleaned_data["email"]).exists():
            form.add_error("email", "Email already exists.")
            is_valid = False

        if is_valid:
            print(form.cleaned_data)
            form.save()
            messages.success(
                request,
                "Account information completed. Now you can verify your email to.",
            )
            return redirect("index")  # redirect to the home page

    return render(request, f"{PREFIX}/comple_account_infomation.html", {"form": form})


def verify_email(request):
    verify_email
    return render(request, f"{PREFIX}/verify_email.html", {})


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

def reset_password_email_sent(request):
    return render(request, f"{PREFIX}/reset_password_email_sent.html")


def process_reset_password(request, token, uidb64):
    try:
        # Giải mã UID từ base64
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user.password = user.information.reset_password

        # Kiểm tra token có hợp lệ không
        if default_token_generator.check_token(user, token):
            print(token)  # In token ra console
            # Bạn có thể thêm logic thay đổi mật khẩu hoặc các thao tác khác ở đây
            return render(
                request, f"{PREFIX}/reset_password_success.html", {"user": user}
            )
        else:
            return render(
                request, f"{PREFIX}/reset_password_invalid.html"
            )  # Nếu token không hợp lệ
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return render(
            request, f"{PREFIX}/reset_password_invalid.html"
        )  # Nếu có lỗi xảy ra
