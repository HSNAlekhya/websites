from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(max_length=100)

    last_name = forms.CharField(max_length=100)

    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )


class LoginForm(forms.Form):

    username = forms.CharField()

    password = forms.CharField(
        widget=forms.PasswordInput
    )


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Order

        fields = [
            'name',
            'phone',
            'address',
            'city',
            'pincode'
        ]

        widgets = {

            'address': forms.Textarea(
                attrs={
                    'rows':4
                }
            )
        }