from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'product_name', 'quantity', 'unit_price', 'status']
        widgets = {
            'customer_name': forms.TextInput(attrs={'placeholder': 'Alex Morgan'}),
            'customer_email': forms.EmailInput(attrs={'placeholder': 'alex@example.com'}),
            'product_name': forms.TextInput(attrs={'placeholder': 'Wireless headphones'}),
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'unit_price': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
        }
