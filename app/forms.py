from typing import Any
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
)
from django.contrib.auth.models import User
from app.models import Product, Category, ProductImage, UserInformation
from ckeditor.widgets import CKEditorWidget
from django.core.validators import MinLengthValidator, RegexValidator, MaxLengthValidator, validate_email

input_attrs = {"class": "form-control"}

class ProductForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields["category"].queryset = user.category_set.all()

    class Meta:
        model = Product
        fields = ["name", "price", "category", "description", "stock"]
        exclude = ["owner"]

        widgets = {
            "name": forms.TextInput(attrs=input_attrs),
            "price": forms.NumberInput(attrs=input_attrs),
            "category": forms.Select(attrs=input_attrs),
            "stock": forms.NumberInput(attrs=input_attrs),
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


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image"]
        exclude = ["product"]
        widgets = {"image": forms.FileInput(attrs={"class": "d-none"})}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        exclude = ["owner"]

        widgets = {"name": forms.TextInput(attrs=input_attrs)}


class AppAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs=input_attrs))
    password = forms.CharField(widget=forms.PasswordInput(attrs=input_attrs))


class UserCreationFormz(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=input_attrs), label="Password",
        help_text="Enter a strong password.",
        validators=[
            # Minimum length of 8 characters
            MinLengthValidator(8),
            # At least one uppercase letter
            RegexValidator(r"^(?=.*[A-Z]).*$", "Must contain at least one uppercase letter."),
            # At least one lowercase letter
            RegexValidator(r"^(?=.*[a-z]).*$", "Must contain at least one lowercase letter."),
            # At least one digit
            RegexValidator(r"^(?=.*\d).*$", "Must contain at least one digit."),
            # At least one special character
            RegexValidator(r"^(?=.*[@$#%^&+=]).*$", "Must contain at least one special character."),
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
        del self.fields['password2']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs=input_attrs),
            "last_name": forms.TextInput(attrs=input_attrs),
            "email": forms.EmailInput(
                attrs={**input_attrs}
            ),
        }
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
        }
       

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Đặt các trường first_name và last_name thành bắt buộc
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

        # Thêm validators cho từng trường
        self.fields["last_name"].validators.extend([
            MaxLengthValidator(50),
            RegexValidator(r'^[a-zA-Z]+$', 'Only letters are allowed.')
        ])
        
        self.fields["first_name"].validators.extend([
            MaxLengthValidator(50),
            RegexValidator(r'^[a-zA-Z]+$', 'Only letters are allowed.')
        ])
        
        self.fields["email"].validators.extend([
            MaxLengthValidator(50),
        ])

        # Kiểm tra nếu email đã tồn tại thì đặt trường này thành readonly
        if self.instance and self.instance.email:
            self.fields["email"].widget.attrs.update({"readonly": True, "disabled": True})
            # Xóa helper_text
            self.fields["email"].help_text = "Please contact the administrator to change your email"

    



class UserInformationForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Tell us about yourself",
            }
        ),
        help_text="Max 50 characters",
    )

    website = forms.URLField(widget=forms.URLInput(attrs=input_attrs))

    class Meta:
        model = UserInformation
        fields = [
            "avatar",
            "phone",
        ]
        widgets = {
            "phone": forms.TextInput(attrs=input_attrs),
        }
        labels = {
            "phone": "Phone number",
        }
        help_texts = {
            "avatar": "Upload an image",
        }


class AppChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs=input_attrs),
        label="Old Password",
        help_text="Enter your current password.",
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=input_attrs),
        label="New Password",
        help_text="Enter a new password.",
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=input_attrs),
        label="Confirm Password",
        help_text="Enter the same password as before, for verification.",
    )


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        label="What is your email?",
        max_length=254,
        widget=forms.EmailInput(attrs=input_attrs),
    )
