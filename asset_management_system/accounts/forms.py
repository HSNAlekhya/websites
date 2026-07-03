from django import forms
from django.contrib.auth.models import User
from .models import Employee

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['phone', 'department']