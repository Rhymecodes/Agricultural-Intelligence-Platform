from django.urls import path
from . import views

urlpatterns = [
    path("", views.weather_calendar_view, name="weather_calendar"),
    path("add-task/", views.add_task, name="add_task"),
    path("delete-task/<int:task_id>/", views.delete_task, name="delete_task"),

]
