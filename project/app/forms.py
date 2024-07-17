from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from app.models import Product, Category


input_attrs = {"class": "form-control"}


class ProductForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields["category"].queryset = user.category_set.all()

    class Meta:
        model = Product
        fields = ["name", "price", "category", "description"]
        exclude = ["owner"]

        widgets = {
            "name": forms.TextInput(attrs=input_attrs),
            "price": forms.NumberInput(attrs=input_attrs),
            "category": forms.Select(attrs=input_attrs),
            "description": forms.Textarea(attrs=input_attrs),
        }

    def save(self, commit: bool = ...) -> Any:
        self.instance.owner = self.user
        return super().save(commit)


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

    class Meta:
        model = User
        fields = ["username", "email"]
        exclude = ["password"]

        widgets = {
            "username": forms.TextInput(attrs=input_attrs),
            "email": forms.EmailInput(attrs=input_attrs),
            "password1": forms.PasswordInput(attrs=input_attrs),
            "password2": forms.PasswordInput(attrs=input_attrs),
        }
