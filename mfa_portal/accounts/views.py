import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .models import UserOTP


def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:

            otp = str(random.randint(100000,999999))

            UserOTP.objects.update_or_create(
                user=user,
                defaults={"otp":otp}
            )

            send_mail(
                "OTP Verification",
                f"Your OTP is {otp}",
                "admin@gmail.com",
                [user.email],
            )

            request.session['user_id'] = user.id

            return redirect('otp')

    return render(request,"accounts/login.html")


def otp_view(request):

    if request.method=="POST":

        otp=request.POST['otp']

        user_id=request.session.get("user_id")

        userotp=UserOTP.objects.get(user_id=user_id)

        if otp==userotp.otp:

            login(request,userotp.user)

            return redirect("dashboard")

    return render(request,"accounts/otp.html")


@login_required
def dashboard(request):

    return render(request,"accounts/dashboard.html")

# Create your views here.
