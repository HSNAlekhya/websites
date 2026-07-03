from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import UserRegisterForm, EmployeeForm
from .models import Employee

def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        emp_form = EmployeeForm(request.POST)

        if user_form.is_valid() and emp_form.is_valid():
            user = User.objects.create_user(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password']
            )

            employee = emp_form.save(commit=False)
            employee.user = user
            employee.save()

            return redirect('login')

    else:
        user_form = UserRegisterForm()
        emp_form = EmployeeForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'emp_form': emp_form
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
