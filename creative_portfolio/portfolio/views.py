from django.shortcuts import render

def home(request):
    return render(request, "portfolio/index.html")

def portfolio(request):
    return render(request, "portfolio/portfolio.html")
# Create your views here.
