from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('register/', views.registerUser, name = 'register'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms and conditions')
]
