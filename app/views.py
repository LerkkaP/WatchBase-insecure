from django.shortcuts import render
from .models import Watch
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
def home(request):
    context = {'is_authenticated': request.session.get('username')}
    return render(request, "home.html", context)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM app_user WHERE username = '{user}'")
            row = cursor.fetchone()
            print(row)
        
        if row and row[2] == password and row[1] == user:
            request.session['username'] = user
            return redirect('home')
        else:
            messages.success(request, ('Invalid username or password'))
            return redirect('login')
    return render(request, "login.html")

@csrf_exempt
def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('login')

def watches(request):
    items = Watch.objects.all()
    return render(request, "watches.html", {"watches": items})

def details(request, id):
    item = Watch.objects.get(id=id)
    return render(request, "details.html", {'watch': item})

def search(request):
    with connection.cursor() as cursor:
        cursor.execute()