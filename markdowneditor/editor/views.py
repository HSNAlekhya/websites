# editor/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from .forms import DocumentForm


# LIST + CREATE PAGE
def index(request):
    documents = Document.objects.all().order_by('-id')

    form = DocumentForm()

    if request.method == "POST":
        form = DocumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request, 'editor/index.html', {
        'documents': documents,
        'form': form
    })


# UPDATE
def edit(request, id):
    document = get_object_or_404(Document, id=id)

    if request.method == "POST":
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DocumentForm(instance=document)

    return render(request, 'editor/edit.html', {
        'form': form,
        'document': document
    })


# DELETE
def delete(request, id):
    document = get_object_or_404(Document, id=id)
    document.delete()
    return redirect('index')