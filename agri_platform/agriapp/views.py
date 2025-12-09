from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FarmerProfile,Crop
from planner.models import FarmTask
from consultations.models import Question
from datetime import date, timedelta
import requests
from django.conf import settings 


# Create your views here.
#Home page
def home (request):
    location = request.GET.get('location', 'Nairobi')
    weather = get_weather(location)
    farming_tip = get_farming_tip_by_weather(weather)
    
    context = {
        'weather': weather,
        'farming_tip': farming_tip,
        'location': location,
        'active_crops': 0,
        'upcoming_tasks': 0,
        'weather_alerts': 0,
        'weekly_forecast': []
    }

    # If user is authenticated, get real data
    if request.user.is_authenticated:
        try:
            farmer_profile = FarmerProfile.objects.get(user=request.user)
            
            # Get active crops count
            today = date.today()
            active_crops = Crop.objects.filter(
                planting_month__lte=today.month,
                harvest_month__gte=today.month
            ).count()
            context['active_crops'] = active_crops
            
            # Get upcoming tasks count (from today onwards)
            upcoming_tasks = FarmTask.objects.filter(
                user=request.user,
                date__gte=today
            ).count()
            context['upcoming_tasks'] = upcoming_tasks
            
        except FarmerProfile.DoesNotExist:
            pass
    
    # Get weather alerts based on conditions
    if weather:
        alerts = get_weather_alerts(weather)
        context['weather_alerts'] = len(alerts)
        context['alerts_list'] = alerts
    
    # Get weekly forecast
    weekly_forecast = get_weekly_forecast(location)
    context['weekly_forecast'] = weekly_forecast
    return render(request, 'home.html', context)

#Login User
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None: 
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong username or Password!')
    
    return render(request, 'auth/login.html')


# Logout User
def user_logout(request):
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

       
    return render(request, 'auth/register.html')

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

def terms_and_conditions(request):
    return render(request, 'terms.html')
def get_weather(location):
    """Get weather data using your API"""
    try:
        # Coordinates for Kenya locations
        coordinates = {
            'Mombasa': {'lat': -4.0435, 'lon': 39.6682},
            'Kwale': {'lat': -4.2500, 'lon': 39.5000},
            'Kilifi': {'lat': -3.6333, 'lon': 39.8500},
            'Tana River': {'lat': -2.5000, 'lon': 40.1667},
            'Lamu': {'lat': -2.2667, 'lon': 40.9000},
            'Taita-Taveta': {'lat': -3.4167, 'lon': 38.3333},
            'Garissa': {'lat': -0.4596, 'lon': 39.6467},
            'Wajir': {'lat': 1.7404, 'lon': 40.0549},
            'Mandera': {'lat': 3.9369, 'lon': 41.8621},
            'Marsabit': {'lat': 2.3170, 'lon': 37.6667},
            'Isiolo': {'lat': 0.3500, 'lon': 37.5833},
            'Meru': {'lat': 0.0505, 'lon': 37.6667},
            'Tharaka-Nithi': {'lat': -0.5000, 'lon': 37.7000},
            'Embu': {'lat': -0.5333, 'lon': 37.4667},
            'Kitui': {'lat': -1.4000, 'lon': 38.2000},
            'Machakos': {'lat': -2.7167, 'lon': 37.2667},
            'Makueni': {'lat': -2.7500, 'lon': 37.7500},
            'Nyandarua': {'lat': -0.5500, 'lon': 36.5500},
            'Nyeri': {'lat': -0.5833, 'lon': 36.9500},
            'Kirinyaga': {'lat': -0.6667, 'lon': 37.4667},
            'Murang\'a': {'lat': -0.7500, 'lon': 37.1667},
            'Kiambu': {'lat': -1.1667, 'lon': 36.8167},
            'Turkana': {'lat': 3.5955, 'lon': 35.8841},
            'West Pokot': {'lat': 1.4000, 'lon': 35.2000},
            'Samburu': {'lat': 2.1629, 'lon': 36.8489},
            'Trans Nzoia': {'lat': 1.0333, 'lon': 35.0333},
            'Uasin Gishu': {'lat': 0.9500, 'lon': 35.3000},
            'Elgeyo-Marakwet': {'lat': 1.1333, 'lon': 35.3167},
            'Nandi': {'lat': 0.4000, 'lon': 35.0500},
            'Baringo': {'lat': 0.6500, 'lon': 35.6667},
            'Laikipia': {'lat': 0.1500, 'lon': 36.5000},
            'Nakuru': {'lat': -0.2833, 'lon': 36.0667},
            'Narok': {'lat': -1.1500, 'lon': 35.8667},
            'Kajiado': {'lat': -2.2500, 'lon': 36.7667},
            'Kericho': {'lat': -0.3667, 'lon': 35.2833},
            'Bomet': {'lat': -0.7962, 'lon': 35.3436},
            'Kakamega': {'lat': 0.2833, 'lon': 34.7500},
            'Vihiga': {'lat': 0.1000, 'lon': 34.7500},
            'Bungoma': {'lat': 0.5641, 'lon': 34.5689},
            'Busia': {'lat': 0.4803, 'lon': 34.1148},
            'Siaya': {'lat': 0.0750, 'lon': 34.2833},
            'Kisumu': {'lat': -0.1019, 'lon': 34.7680},
            'Homa Bay': {'lat': -0.5000, 'lon': 34.4667},
            'Migori': {'lat': -1.0667, 'lon': 34.4667},
            'Kisii': {'lat': -0.6833, 'lon': 34.7667},
            'Nyamira': {'lat': -0.6000, 'lon': 34.8500},
            'Nairobi': {'lat': -1.2921, 'lon': 36.8219},
        }
        
        if location in coordinates:
            coords = coordinates[location]
            api_key = settings.WEATHER_API_KEY
            
            # Using OpenWeatherMap API (replace with your API provider if different)
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                "lat": coords['lat'],
                "lon": coords['lon'],
                "appid": api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'rainfall': data.get('rain', {}).get('1h', 0),
                'weather': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
            }
    except Exception as e:
        print(f"Weather API error: {e}")
        return None

def get_weekly_forecast(location):
    """Get 7-day weather forecast"""
    try:
        coordinates = {
            'Mombasa': {'lat': -4.0435, 'lon': 39.6682},
            'Nairobi': {'lat': -1.2921, 'lon': 36.8219},
            # Add all other locations as needed (same as above)
        }
        
        if location not in coordinates:
            # Try to find partial match
            for key in coordinates:
                if location.lower() in key.lower():
                    location = key
                    break
        
        if location in coordinates:
            coords = coordinates[location]
            api_key = settings.WEATHER_API_KEY
            
            url = f"https://api.openweathermap.org/data/2.5/forecast"
            params = {
                "lat": coords['lat'],
                "lon": coords['lon'],
                "appid": api_key,
                "units": "metric",
                "cnt": 40  # 5 days of 3-hourly data
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            # Process forecast data to get daily forecast
            forecast_dict = {}
            for item in data['list']:
                date_str = item['dt_txt'].split()[0]
                
                if date_str not in forecast_dict:
                    forecast_dict[date_str] = {
                        'date': date_str,
                        'temp_max': item['main']['temp_max'],
                        'temp_min': item['main']['temp_min'],
                        'weather': item['weather'][0]['main'],
                        'description': item['weather'][0]['description'],
                        'rainfall': item.get('rain', {}).get('3h', 0),
                    }
                else:
                    # Keep max/min
                    forecast_dict[date_str]['temp_max'] = max(
                        forecast_dict[date_str]['temp_max'],
                        item['main']['temp_max']
                    )
                    forecast_dict[date_str]['temp_min'] = min(
                        forecast_dict[date_str]['temp_min'],
                        item['main']['temp_min']
                    )
            
            # Return sorted forecast (next 7 days)
            return sorted(list(forecast_dict.values()), key=lambda x: x['date'])[:7]
    
    except Exception as e:
        print(f"Weekly forecast error: {e}")
        return []


def get_weather_alerts(weather):
    """Generate alerts based on weather conditions"""
    alerts = []
    
    if not weather:
        return alerts
    
    temp = weather.get('temperature', 0)
    humidity = weather.get('humidity', 0)
    rainfall = weather.get('rainfall', 0)
    weather_type = weather.get('weather', '').lower()
    
    # Temperature alerts
    if temp > 35:
        alerts.append({
            'type': 'danger',
            'icon': '🌡️',
            'message': f'Extreme heat alert! Temperature is {temp}°C. Increase irrigation.'
        })
    elif temp > 30:
        alerts.append({
            'type': 'warning',
            'icon': '☀️',
            'message': f'Hot weather ({temp}°C). Monitor crops for heat stress.'
        })
    
    if temp < 5:
        alerts.append({
            'type': 'danger',
            'icon': '❄️',
            'message': f'Frost risk! Temperature is {temp}°C. Protect sensitive crops.'
        })
    
    # Rainfall alerts
    if 'rain' in weather_type or rainfall > 5:
        alerts.append({
            'type': 'info',
            'icon': '🌧️',
            'message': f'Heavy rainfall expected ({rainfall}mm). Watch for waterlogging.'
        })
    
    # Humidity alerts
    if humidity > 85:
        alerts.append({
            'type': 'warning',
            'icon': '💧',
            'message': f'Very high humidity ({humidity}%). Risk of fungal diseases.'
        })
    
    if humidity < 30:
        alerts.append({
            'type': 'warning',
            'icon': '💨',
            'message': f'Low humidity ({humidity}%). Increase watering frequency.'
        })
    
    return alerts

def get_farming_tip_by_weather(weather):
    """Get farming tip based on actual weather conditions"""
    if not weather:
        return "Monitor your crops regularly and keep them well-watered."
    
    temp = weather.get('temperature', 0)
    humidity = weather.get('humidity', 0)
    rainfall = weather.get('rainfall', 0)
    weather_type = weather.get('weather', '').lower()
    
    # Tips based on weather conditions
    if 'rain' in weather_type or rainfall > 0:
        return " Rain detected! This is good for your crops. Ensure proper drainage to prevent waterlogging."
    
    if temp > 30:
        return " Hot weather ahead. Increase irrigation frequency. Mulch your soil to retain moisture."
    
    if temp < 15:
        return " Cold temperatures. Protect sensitive crops. Consider using row covers if frost is expected."
    
    if humidity > 80:
        return " High humidity. Monitor for fungal diseases. Improve air circulation in your crops."
    
    if humidity < 30:
        return " Low humidity and dry conditions. Water your crops early in the morning or late evening to minimize evaporation."
    
    if 15 <= temp <= 25 and 50 <= humidity <= 70:
        return " Perfect farming weather! Ideal conditions for most crops. Great time for planting or weeding."
    
    return " Keep monitoring your crops and adjust care based on changing weather conditions."

