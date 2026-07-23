from django import forms

from .models import Coupon


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ('code', 'description', 'discount_type', 'discount_value', 'minimum_purchase', 'usage_limit', 'starts_at', 'expires_at', 'is_active')
        widgets = {
            'starts_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'discount_value': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'}),
            'minimum_purchase': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
            'usage_limit': forms.NumberInput(attrs={'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
        self.fields['is_active'].widget.attrs['class'] = 'form-check-input'

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()