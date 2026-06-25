from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'name',
            'email',
            'booking_date',
            'booking_time'
        ]

        widgets = {
            'booking_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'booking_time': forms.TimeInput(
                attrs={'type': 'time'}
            ),
        }