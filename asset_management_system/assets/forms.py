from django import forms
from .models import Asset, AssetRequest

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'asset_type', 'serial_number', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asset Name'}),
            'asset_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type (e.g., Laptop, Desk)'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial Number'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Available/In-Use'}),
        }


class RequestForm(forms.ModelForm):
    class Meta:
        model = AssetRequest
        fields = ['asset']
        widgets = {
            'asset': forms.Select(attrs={'class': 'form-control'}),
        }