from django import forms

class MessageForm(forms.Form):
    username = forms.CharField(max_length=50)
    text = forms.CharField(max_length=200)