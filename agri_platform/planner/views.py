from django.shortcuts import render, redirect, get_object_or_404
from .models import FarmTask
from datetime import datetime, date
import calendar as cal_module  # avoid conflict with app name

# Calendar view
def calendar_view(request):
    month = request.GET.get('month')
    year = request.GET.get('year')
    today = date.today()
    
    now = datetime.now()
    if month and year:
        month = int(month)
        year = int(year)
    else:
        month = now.month
        year = now.year

    cal = cal_module.Calendar(firstweekday=0)
    month_days = cal.itermonthdays(year, month)
    weeks = []
    week = []
    for day in month_days:
        week.append(day)
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:
        weeks.append(week)

    prev_month = month - 1
    prev_year = year
    if prev_month < 1:
        prev_month = 12
        prev_year -= 1

    next_month = month + 1
    next_year = year
    if next_month > 12:
        next_month = 1
        next_year += 1

    # Get tasks for the current month
    tasks = FarmTask.objects.filter(user=request.user, date__year=year, date__month=month).order_by('date')
    
    upcoming_tasks = FarmTask.objects.filter(
        user=request.user,
        date__gte=today
    ).order_by('date')[:6]

    context = {
        'weeks': weeks,
        'month': month,
        'year': year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'month_name': cal_module.month_name[month],
        'tasks': tasks,
        'upcoming_tasks': upcoming_tasks,

    }
    return render(request, 'planner/calendar.html', context)


# Add task view
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('task_name')
        task_date = request.POST.get('task_date')
        task_type = request.POST.get('task_type')

        if title and task_date:
            FarmTask.objects.create(
                user=request.user,
                title=title,
                date=task_date,
                task_type=task_type
            )

        return redirect('calendar_view')
    return render(request, 'planner/add_task.html')


# Delete task view
def delete_task(request, task_id):
    task = get_object_or_404(FarmTask, id=task_id, user=request.user)
    task.delete()
    return redirect('calendar_view')
