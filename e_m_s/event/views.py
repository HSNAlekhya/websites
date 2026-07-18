from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .models import Event


@login_required(login_url='login')
def home(request):
    events = Event.objects.order_by('date')
    registered_users = User.objects.order_by('username')
    registrations_count = registered_users.count()
    return render(request, 'event/home.html', {
        'events': events,
        'registered_users': registered_users,
        'registrations_count': registrations_count,
    })


@login_required(login_url='login')
def event_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        date = request.POST.get('date')
        status = request.POST.get('status', 'Planned').strip()

        if title and date:
            Event.objects.create(title=title, description=description, date=date, status=status)
            return redirect('home')

    return render(request, 'event/create_event.html')


@login_required(login_url='login')
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event/event_detail.html', {'event': event})


@login_required(login_url='login')
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        event.title = request.POST.get('title', '').strip()
        event.description = request.POST.get('description', '').strip()
        event.date = request.POST.get('date')
        event.status = request.POST.get('status', 'Planned').strip()

        if event.title and event.date:
            event.save()
            return redirect('event-detail', pk=event.pk)

    return render(request, 'event/event_form.html', {'event': event, 'mode': 'Update'})


@login_required(login_url='login')
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'event/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'event/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
