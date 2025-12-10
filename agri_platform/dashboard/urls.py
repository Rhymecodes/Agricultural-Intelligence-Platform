from django.urls import path
from . import views


app_name = 'dashboard'


urlpatterns = [
path('', views.dashboard_home, name='home'),


# CRUD lists
path('farmers/', views.farmers_list, name='farmers_list'),
path('farmers/add/', views.farmer_create, name='farmer_add'),
path('farmers/<int:pk>/edit/', views.farmer_edit, name='farmer_edit'),
path('farmers/<int:pk>/delete/', views.farmer_delete, name='farmer_delete'),


path('plants/', views.plant_list, name='plant_list'),
path('plants/add/', views.plant_create, name='plant_add'),
path('plants/<int:pk>/edit/', views.plant_edit, name='plant_edit'),
path('plants/<int:pk>/delete/', views.plant_delete, name='plant_delete'),


path('pests/', views.pests_list, name='pests_list'),
path('pests/add/', views.pest_create, name='pest_add'),
path('pests/<int:pk>/edit/', views.pest_edit, name='pest_edit'),
path('pests/<int:pk>/delete/', views.pest_delete, name='pest_delete'),


path('tips/', views.tips_list, name='tips_list'),
path('tips/<int:pk>/delete/', views.tip_delete, name='tip_delete'),


path('consultations/', views.consultations_list, name='consultations_list'),
path('payments/', views.payments_list, name='payments_list'),

 
path('confirm-delete/', views.confirm_delete, name='confirm_delete'),

]
