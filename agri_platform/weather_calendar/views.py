from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
from .models import FarmTask
from django.conf import settings
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

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