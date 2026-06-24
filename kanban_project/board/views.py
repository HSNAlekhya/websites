from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

def board_view(request):
    context = {
        'todo_tasks': Task.objects.filter(status='todo'),
        'doing_tasks': Task.objects.filter(status='doing'),
        'done_tasks': Task.objects.filter(status='done'),
    }
    return render(request, 'board/board.html', context)

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('board')
    else:
        form = TaskForm()

    return render(request, 'board/create_task.html', {'form': form})

def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('board')
    else:
        form = TaskForm(instance=task)

    return render(request, 'board/edit_task.html', {
        'form': form,
        'task': task
    })

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('board')

    return render(request, 'board/delete_task.html', {
        'task': task
    })

# Create your views here.
