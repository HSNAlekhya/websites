import calendar
from datetime import datetime

from django.shortcuts import render, redirect

from .forms import BookingForm


def booking_calendar(request):

    today = datetime.today()

    year = int(
        request.GET.get("year", today.year)
    )

    month = int(
        request.GET.get("month", today.month)
    )

    cal = calendar.monthcalendar(year, month)

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("success")

    else:
        form = BookingForm()

    context = {
        "calendar": cal,
        "month": month,
        "year": year,
        "month_name": calendar.month_name[month],
        "form": form,
    }

    return render(
        request,
        "booking/calendar.html",
        context
    )


def success(request):
    return render(
        request,
        "booking/success.html"
    )

# Create your views here.
