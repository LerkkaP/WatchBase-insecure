from django.shortcuts import render
from .models import Watch
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def home(request):
    results = []
    context = {'is_authenticated': request.session.get('username')}

    search_query = request.GET.get('search')
    if search_query:
       with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM app_watch WHERE brand LIKE '%{search_query}%'")
            filtered_watches = cursor.fetchall()
            for alkio in filtered_watches:
                items = {"id": alkio[0], "brand": alkio[1], "model": alkio[3], "price": alkio[2]}
                results.append(items)
            context['filtered_watches'] = results
        #filtered_watches = Watch.objects.filter(Q(brand__icontains=search_query) | Q(model__icontains=search_query))
        #context['filtered_watches'] = filtered_watches

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

     