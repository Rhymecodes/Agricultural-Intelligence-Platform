from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
from .models import FarmTask
from django.conf import settings
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from datetime import datetime
from calendar import monthcalendar, month_name
from agriapp.models import FarmerProfile
from agriapp.views import get_weather, get_farming_tip_by_weather

# Create your views here.
@login_required
def weather_calendar_view(request):
    weather_data = None
    location = None

    if request.method == "POST":
        location = request.POST.get("county") 
        if location == 'other':
            location = request.POST.get('custom_location') # adjust if you use dropdown + manual input

        url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()

    # Tasks for the logged-in user
    tasks = FarmTask.objects.filter(user=request.user).order_by("date")

    # Convert tasks to JSON for FullCalendar
    tasks_json = json.dumps([
        {
            "title": task.title,
            "start": task.date.strftime("%Y-%m-%d"),
            "description": task.description
        } for task in tasks
    ], cls=DjangoJSONEncoder)

    # Calendar logic
    now = datetime.now()
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')
    
    # Handle empty or invalid values
    try:
        year = int(year) if year else now.year
        month = int(month) if month else now.month
    except ValueError:
        year = now.year
        month = now.month
    
    cal = monthcalendar(year, month)
    month_name_str = month_name[month]
    
    all_tasks = FarmTask.objects.filter(user=request.user)
    
    tasks_by_date = {}
    for task in all_tasks:
        date_key = task.date.isoformat()
        if date_key not in tasks_by_date:
            tasks_by_date[date_key] = []
        tasks_by_date[date_key].append(task)
    
    calendar_with_tasks = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append({'day': 0, 'tasks': []})
            else:
                date_obj = datetime(year, month, day).date()
                date_key = date_obj.isoformat()
                is_today = date_obj == now.date()
                week_data.append({
                    'day': day,
                    'tasks': tasks_by_date.get(date_key, []),
                    'is_today': is_today,
                    'date': date_obj
                })
        calendar_with_tasks.append(week_data)
    
    today = now.date()
    upcoming_tasks = FarmTask.objects.filter(
        user=request.user,
        date__gte=today,
    ).order_by('date')[:10]
    
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year
    
    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year
    
    context = {
        'weather': get_weather,
        'farming_tip': get_farming_tip_by_weather,
        'location': location,
        'calendar': calendar_with_tasks,
        'month': month,
        'year': year,
        'month_name': month_name_str,
        'today': now.date(),
        'upcoming_tasks': upcoming_tasks,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'farmer_profile': FarmerProfile,
    }
    
    return render(request, "weather_calendar/weather_calendar.html", {
        "weather": weather_data,
        "location": location,
        "tasks": tasks,
        "tasks_json": tasks_json
    })

    

# ADD TASK
@login_required
def add_task(request):
    if request.method == "POST":
        FarmTask.objects.create(
            user=request.user,
            title=request.POST["title"],
            date=request.POST["date"],
            description=request.POST.get("description", "")
        )
    return redirect("weather_calendar")

# DELETE TASK
@login_required
def delete_task(request, task_id):
    task = FarmTask.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect("weather_calendar")