from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm

def home(request):
    return render(request, 'home.html')

def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments')
    else:
        form = AppointmentForm()

    return render(request, 'add_appointment.html', {'form': form})

def appointments(request):
    data = Appointment.objects.all()
    return render(request, 'appointments.html', {'appointments': data})

# Create your views here.
