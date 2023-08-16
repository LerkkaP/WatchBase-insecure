from django.shortcuts import render
from .models import Watch
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

# Create your views here.
def home(request):
    return render(request, "home.html")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM app_user')
            for row in cursor:
                user_real = row[1]
                password_real = row[2]
        if user == user_real and password == password_real:
            print("toimii")
        else:
            print("incorrect password or username")

    return render(request, "login.html")

def watches(request):
    items = Watch.objects.all()
    return render(request, "watches.html", {"watches": items})

