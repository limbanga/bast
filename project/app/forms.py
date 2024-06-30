from django import forms
from app.models import Product, Category


input_attrs = {
    "class": "form-control"
}

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description"]
        exclude = ["owner"]

        widgets = {
            "name": forms.TextInput(attrs=input_attrs),
            "price": forms.NumberInput(attrs=input_attrs),
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