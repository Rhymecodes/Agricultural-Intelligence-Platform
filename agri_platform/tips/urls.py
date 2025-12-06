from django.urls import path
from . import views

urlpatterns = [
    path('', views.tips_list, name='tips_list'),
    path('create/', views.create_tip, name='create_tip'),
    path('<int:pk>/', views.tip_detail, name='tip_detail'),
    path('<int:pk>/like/', views.like_tip, name='like_tip'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
]