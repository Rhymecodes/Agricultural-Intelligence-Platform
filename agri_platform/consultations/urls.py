from django.urls import path
from . import views

urlpatterns = [
    path('', views.consultations_home, name='consultations_home'),
    path('ask/', views.ask_question, name='ask_question'),
    path('book/', views.book_consultation, name='book_consultation'),
    path('mpesa/<int:consultation_id>/', views.mpesa_payment, name='mpesa_payment'),
    path('callback/', views.mpesa_callback, name='mpesa_callback'),
    path('forum/', views.qa_forum, name='qa_forum')
]