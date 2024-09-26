from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Department, Doctor_details, appointment
from django.db.models import Q
from datetime import datetime


def check_appoinment( uid , appointment_date, appoinment_count):
    qs = appointment.objects.filter(
        appointment_date__lte = appointment_date,
        doctor__uid = uid,
    )
    if qs.count() >= appoinment_count:
        return False
    
    # Otherwise, return False (unavailable)
    return True
def home(request):
    department_objs = Department.objects.all()
    doctor_objs = Doctor_details.objects.all()
    search = request.GET.get('search')

    if search:
        doctor_objs = doctor_objs.filter(Q(doctors_name__icontains = search) | Q(description__icontains = search))
    
    if search:
        department_objs = department_objs.filter(dep_name__icontains = search)

    context = {'department_objs':department_objs, 'doctor_objs':doctor_objs, 'search':search}
    return render(request, 'home.html', context)


def doctors_details(request, uid):
    doctor_obj = Doctor_details.objects.get(uid=uid)

    if request.method == 'POST':
        appointment_date_str = request.POST.get('appointment_date')

        # Print the appointment date to see what is being sent
        print("Appointment Date Received: ", appointment_date_str)

        if not appointment_date_str:
            return render(request, 'doctors_details.html', {
                'doctor_obj': doctor_obj,
                'error': "Please provide an appointment date."
            })
        
        # Parse the appointment date into a datetime object
        try:
            appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'doctors_details.html', {
                'doctor_obj': doctor_obj,
                'error': "Invalid date format. Please use YYYY-MM-DD."
            })

        # Check if the appointment limit is exceeded
        if not check_appoinment(uid, appointment_date, doctor_obj.appoinment_count):
              return render(request, 'doctors_details.html', {
                'doctor_obj': doctor_obj,
                'availble': "Appointment not available on that day"
            })
          
          
        # Create the appointment using the provided date
        appointment.objects.create(
            doctor=doctor_obj, 
            appointment_date=appointment_date, 
            user=request.user
        )
        return redirect('home')

    context = {'doctor_obj': doctor_obj}
    return render(request, 'doctors_details.html', context)


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


