from django import forms
from .models import ProductAdd

class ProductAddForm(forms.ModelForm):
    class Meta:
        model = ProductAdd
        fields = ['name', 'info_title', 'info', 'amount', 'unit', 'price', 'currency']