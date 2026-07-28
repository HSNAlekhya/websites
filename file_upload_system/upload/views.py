from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import FileUpload

def home(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FileUploadForm()

    files = FileUpload.objects.all()

    return render(request, 'upload/home.html', {
        'form': form,
        'files': files
    })

# Create your views here.
