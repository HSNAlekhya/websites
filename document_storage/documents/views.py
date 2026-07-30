from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from .forms import DocumentForm


def home(request):
    docs = Document.objects.all()

    return render(request, "documents/home.html", {
        "docs": docs
    })


def upload_document(request):

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = DocumentForm()

    return render(request, "documents/upload.html", {
        "form": form
    })


def update_document(request, id):

    doc = get_object_or_404(Document, id=id)

    if request.method == "POST":
        form = DocumentForm(
            request.POST,
            request.FILES,
            instance=doc
        )

        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = DocumentForm(instance=doc)

    return render(request, "documents/update.html", {
        "form": form
    })


def delete_document(request, id):

    doc = get_object_or_404(Document, id=id)

    if request.method == "POST":
        doc.delete()
        return redirect("home")

    return render(request, "documents/delete.html", {
        "doc": doc
    })

# Create your views here.
