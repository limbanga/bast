from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from app.models import Product, Category, ProductImage, UserInformation
from ckeditor.widgets import CKEditorWidget


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


class AppUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=input_attrs), label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=input_attrs), label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

        widgets = {
            "username": forms.TextInput(attrs=input_attrs),
            "email": forms.EmailInput(attrs=input_attrs),
            "first_name": forms.TextInput(attrs=input_attrs),
            "last_name": forms.TextInput(attrs=input_attrs),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs=input_attrs),
            "last_name": forms.TextInput(attrs=input_attrs),
            "email": forms.EmailInput(
                attrs={**input_attrs, "readonly": True, "disabled": True}
            ),
        }
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
        }
        help_texts = {
            "email": "Email cannot be changed",
        }


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

