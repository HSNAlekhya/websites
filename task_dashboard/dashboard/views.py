from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

def dashboard(request):
    total = Task.objects.count()
    completed = Task.objects.filter(status='Completed').count()
    pending = Task.objects.filter(status='Pending').count()

    percent = 0
    if total > 0:
        percent = (completed / total) * 100

    context = {
        'total': total,
        'completed': completed,
        'pending': pending,
        'percent': round(percent, 2)
    }
    return render(request, 'dashboard.html', context)


def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'task_list.html', {'tasks': tasks})


def add_task(request):
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')

    return render(request, 'add_task.html', {'form': form})

# Create your views here.
