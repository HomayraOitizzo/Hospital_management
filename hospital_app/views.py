from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_objs = User.objects.filter(username = username)

        if not user_objs.exists():
            return render(request, 'login.html', {'error': "user not found"})
        user_objs = authenticate(username = username, password = password)

        if not user_objs:
          context = {'error': 'Invalid password'}
          return render(request, 'login.html', context)
        login(request, user_objs)
        return redirect('/') 
    
    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_objs = User.objects.filter(username = username)

        if user_objs.exists():
            return render(request, 'register.html', {'error1': 'user already exists'})
        user = User.objects.create(username = username)

        user.set_password(password)
        user.save()
        return redirect('/')        




    return render(request, 'register.html')


