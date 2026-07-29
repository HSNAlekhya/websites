from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import FriendRequest, Friend
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    users = User.objects.exclude(id=request.user.id)

    friend, created = Friend.objects.get_or_create(user=request.user)

    friends = friend.friends.all()

    sent = FriendRequest.objects.filter(
        from_user=request.user
    ).values_list("to_user", flat=True)

    return render(request, "frd_req/home.html", {
        "users": users,
        "friends": friends,
        "sent": sent,
    })

@login_required
def send_request(request, id):
    user = get_object_or_404(User, id=id)

    FriendRequest.objects.get_or_create(
        from_user=request.user,
        to_user=user
    )

    return redirect("home")

@login_required
def requests(request):
    reqs = FriendRequest.objects.filter(to_user=request.user)

    return render(request, "frd_req/requests.html", {
        "requests": reqs
    })

@login_required
def accept_request(request, id):
    req = get_object_or_404(FriendRequest, id=id)

    me = Friend.objects.get(user=request.user)
    other = Friend.objects.get(user=req.from_user)

    me.friends.add(req.from_user)
    other.friends.add(request.user)

    req.delete()

    return redirect("requests")

@login_required
def delete_request(request, id):
    req = get_object_or_404(FriendRequest, id=id)
    req.delete()
    return redirect("requests")

@login_required
def remove_friend(request, id):
    user = get_object_or_404(User, id=id)

    me = Friend.objects.get(user=request.user)
    other = Friend.objects.get(user=user)

    me.friends.remove(user)
    other.friends.remove(request.user)

    return redirect("home")

# Create your views here.
