from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as _login, logout as _logout
from django.contrib import messages
from app.forms import (
    AppAuthenticationForm,
    UserCreationFormz,
    AppChangePasswordForm,
    ResetPasswordForm,
    UserForm
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

# Pass
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
    form = UserCreationFormz()
    if request.method == "POST":
        form = UserCreationFormz(request.POST)
        if form.is_valid():
            user = form.save()
            user_information = UserInformation(user=user)
            user_information.save()
            # log the user in
            _login(request, user)
            return redirect("comple_account_infomation")  # redirect to the home page
        else:
            print(form.errors)
    return render(request, f"{PREFIX}/register.html", {"form": form})

@login_required
def comple_account_infomation(request):
    # Check if user has email
    if request.user.email:
        return redirect('index')

    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)
        print('form.is_valid():',form.is_valid())
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect("index")  # redirect to the home page
        else:
            print(form.errors)

    return render(request, f"{PREFIX}/comple_account_infomation.html", {"form": form})

def verify_email(request):
    verify_email
    return render(request, f"{PREFIX}/verify_email.html", {})

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
                print(user)
                print(user.information)
                # send email
                messages.success(request, "Email sent.")
                # TODO: Test this later when have email setup
                reset_password = generate_random_password()
                user_information = user.information
                user_information.reset_password = reset_password
                user_information.save()
                
                # Tạo token
                token = default_token_generator.make_token(user)

                # Mã hóa User ID thành Base64 để sử dụng trong URL
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                print(f'Token: {token}')
                print(f'UIDB64: {uidb64}')

                subject = "BAST - Reset Password"
                host_name = request.get_host()
                active_link = f"http://{host_name}/auth/reset_password/{token}/{uidb64}"
                
                message_to_sent = (
                    f"You new password is: {reset_password}"+
                    f"Click here to reset your password: {active_link}."
                    + " If you did not request this, please ignore this email."
                )
                print(active_link)

                print(message_to_sent)
                # send_mail(
                #     subject,
                #     message_to_sent,
                #     settings.DEFAULT_FROM_EMAIL,
                #     [user.email],
                #     fail_silently=False,
                # )
                return redirect("reset_password_email_sent")
            except User.DoesNotExist:
                messages.error(request, "User not found.")
                form.add_error(None, "User not found.")

        else:
            print(form.errors)

    return render(request, f"{PREFIX}/reset_password.html", {"form": form})


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
            return render(request, f"{PREFIX}/reset_password_success.html", {'user': user})
        else:
            return render(request, f"{PREFIX}/reset_password_invalid.html")  # Nếu token không hợp lệ
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return render(request, f"{PREFIX}/reset_password_invalid.html")  # Nếu có lỗi xảy ra