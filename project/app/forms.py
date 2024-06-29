from django import forms
from app.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description"]
        exclude = ["owner"]
