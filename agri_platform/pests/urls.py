from django.urls import path
from . import views

urlpatterns = [
    path('', views.plant_list, name='plant_list'),  # List all plants
    path('<int:plant_id>/', views.plant_detail, name='plant_detail'),  # Details for a plant
    path('diagnose/', views.pest_diagnosis, name='pest_diagnosis'),
]
