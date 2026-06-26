from django.shortcuts import render, redirect
from .models import Message
from .forms import MessageForm

def chat_room(request):

    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            Message.objects.create(
                username=form.cleaned_data["username"],
                text=form.cleaned_data["text"]
            )
            return redirect("chat")

    else:
        form = MessageForm()

    messages = Message.objects.all()

    return render(
        request,
        "chat/room.html",
        {
            "form": form,
            "messages": messages
        }
    )

# Create your views here.
