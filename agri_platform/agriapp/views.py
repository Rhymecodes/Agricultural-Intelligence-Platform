from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FarmerProfile



# Create your views here.
#Home page
def home (request):
    return render(request, 'home.html')

#Login User
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = f'_{username}')
        except:
            print('User not found!')

        user = authenticate(request, username=username, password=password)

        if user is not None: 
             login(request, user)
             return redirect('dashboard')
        else:
            messages.error(request, 'Wrong username or Password!')
    context = {}
    return render(request, 'agriapp/login_form.html', context)


# Logout User
def logout(request):
    context ={}
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

#Register User
def registerUser(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        password = request.POST.get('password')
        password2 = request.POST.get('Repeat Password')

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        
         # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Create farmer profile
        FarmerProfile.objects.create(
            user=user,
            phone=phone,
            location=location
        )
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')

       
    return render(request, 'agriapp/register_form.html', context)

# Dashboard (requires login)
@login_required(login_url='login')
def dashboard(request):
    try:
        farmer_profile = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        farmer_profile = None
    
    context = {
        'farmer_profile': farmer_profile
    }
    return render(request, 'dashboard.html', context)
