from typing import Any
import re
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django.contrib.auth.models import User
from app.models import Product, Category, ProductImage, UserInformation, Address
from ckeditor.widgets import CKEditorWidget
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
    MaxLengthValidator,
    validate_email,
)
from allauth.account.forms import (
    SignupForm,
    LoginForm,
    ResetPasswordForm,
    ChangePasswordForm,
)

input_attrs = {"class": "form-control rounded-0"}


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(input_attrs)
            if self.fields[field].required:
                self.fields[field].label = f"{self.fields[field].label} *"


class ProductForm(BaseForm):

    def __init__(self, user, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields["category"].queryset = user.category_set.all()

    class Meta:
        model = Product
        fields = ["name", "price", "category", "description", "stock"]
        exclude = ["owner"]

        widgets = {
            "price": forms.NumberInput(attrs={**input_attrs, "step": "1"}),
            "description": forms.CharField(
                widget=CKEditorWidget(
                    config_name="default",
                )
            ),
        }

        labels = {
            "name": "Product Name",
            "price": "Price",
            "category": "Category",
            "description": "Description",
            "stock": "Stock",
        }

    def save(self, commit: bool = ...) -> Any:
        self.instance.owner = self.user
        return super().save(commit)

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock < 1:
            raise forms.ValidationError("Stock must be greater than or equal to 1.")
        return stock


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image"]
        exclude = ["product"]
        widgets = {"image": forms.FileInput(attrs={"class": "d-none"})}


class CategoryForm(BaseForm):
    class Meta:
        model = Category
        fields = ["name"]
        exclude = ["owner"]

        labels = {"name": "Category Name"}

        help_texts = {"name": "Max 50 characters"}


class AppAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs=input_attrs))
    password = forms.CharField(widget=forms.PasswordInput(attrs=input_attrs))

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=input_attrs),
        label="Password",
        help_text="Enter a strong password.",
        validators=[
            # Minimum length of 8 characters
            MinLengthValidator(8),
            # At least one uppercase letter
            RegexValidator(
                r"^(?=.*[A-Z]).*$", "Must contain at least one uppercase letter."
            ),
            # At least one lowercase letter
            RegexValidator(
                r"^(?=.*[a-z]).*$", "Must contain at least one lowercase letter."
            ),
            # At least one digit
            RegexValidator(r"^(?=.*\d).*$", "Must contain at least one digit."),
            # At least one special character
            RegexValidator(
                r"^(?=.*[@$#%^&+=]).*$", "Must contain at least one special character."
            ),
        ],
    )

    class Meta:
        model = User
        fields = ["username"]

        widgets = {
            "username": forms.TextInput(attrs=input_attrs),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ignore 'password2' field


class UserForm(BaseForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs=input_attrs),
            "last_name": forms.TextInput(attrs=input_attrs),
            "email": forms.EmailInput(attrs={**input_attrs}),
        }
        labels = {
            "first_name": "Tên",
            "last_name": "Họ",
            "email": "Email",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Đặt các trường first_name và last_name thành bắt buộc
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

        validator_name = RegexValidator(
            r"^[\w\s]+$", "Only letters are allowed.", flags=re.UNICODE
        )
        # Thêm validators cho từng trường
        self.fields["last_name"].validators.extend(
            [MaxLengthValidator(50), validator_name]
        )

        self.fields["first_name"].validators.extend(
            [MaxLengthValidator(50), validator_name]
        )

        self.fields["email"].validators.extend(
            [
                MaxLengthValidator(50),
            ]
        )

        # Kiểm tra nếu email đã tồn tại thì đặt trường này thành readonly
        if self.instance and self.instance.email:
            self.fields["email"].widget.attrs.update(
                {"readonly": True, "disabled": True}
            )
            # Xóa helper_text
            self.fields["email"].help_text = (
                "Please contact the administrator to change your email"
            )


class UserInformationForm(BaseForm):

    class Meta:
        model = UserInformation
        fields = [
            "avatar",
            "phone",
            "bio",
        ]   
        widgets = {
            "phone": forms.TextInput(attrs=input_attrs),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Hãy viết một chút về bản thân bạn",
                }
            ),
        }
        labels = {
            "phone": "Số điện thoại",
            "bio": "Giới thiệu ngắn",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].validators.extend(
            [
                RegexValidator(
                    r"^\+?1?\d{9,15}$",
                    "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                )
            ]
        )


class ChangePasswordFormz(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(input_attrs)
            if self.fields[field].required:
                self.fields[field].label = f"{self.fields[field].label} *"

        self.fields["password1"].help_text = ""


class ResetPasswordFormz(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(input_attrs)


class SignupFormz(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["password2"]
        self.fields["password1"].help_text = "Enter a strong password."
        for field in self.fields:
            self.fields[field].widget.attrs.update(input_attrs)

    def save(self, request):
        user = super().save(request)
        user.save()
        return user


class LoginFormz(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        formatedFields = ["login", "password"]
        for field in formatedFields:
            self.fields[field].label = self.fields[field].label.capitalize()
            self.fields[field].widget.attrs.update(input_attrs)
        self.fields["password"].help_text = ""

    def clean_username(self):
        # Xử lý nếu cần
        username = self.cleaned_data.get("username")
        # Kiểm tra nếu login bằng email thay vì username
        return username


class AddressForm(BaseForm):
    class Meta:
        model = Address
        fields = "__all__"
        exclude = ["owner"]

        labels = {
            "province": "Tỉnh/Thành phố",
            "district": "Quận/Huyện",
            "ward": "Phường/Xã",
            "extra_description": "Địa chỉ cụ thể",
        }

        help_texts = {
            "province": "Xin hãy chọn tỉnh/thành phố",
            "district": "Xin hãy chọn quận/huyện",
            "ward": "Xin hãy chọn phường/xã",
            "extra_description": "Mô tả thêm (nếu có)",
        }
