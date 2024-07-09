from django import forms
from django.contrib.auth.forms import AuthenticationForm
from app.models import Product, Category


input_attrs = {
    "class": "form-control"
}

class ProductForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = user.category_set.all()

    class Meta:
        model = Product
        fields = ["name", "price", "category" ,"description"]
        exclude = ["owner"]

        widgets = {
            "name": forms.TextInput(attrs=input_attrs),
            "price": forms.NumberInput(attrs=input_attrs),
            "category": forms.Select(attrs=input_attrs),
            "description": forms.Textarea(attrs=input_attrs)
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        exclude = ["owner"]

        widgets = {
            "name": forms.TextInput(attrs=input_attrs)
        }

class AppAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs=input_attrs))
    password = forms.CharField(widget=forms.PasswordInput(attrs=input_attrs))