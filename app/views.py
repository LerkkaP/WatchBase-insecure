from django.shortcuts import render, HttpResponse
from .models import Watch

# Create your views here.
def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def watches(request):
    items = Watch.objects.all()
    return render(request, "watches.html", {"watches": items})

