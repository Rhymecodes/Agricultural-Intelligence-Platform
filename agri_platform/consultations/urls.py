from django.urls import path
from . import views

urlpatterns = [
    # Q&A Forum
    path('', views.qa_forum, name='qa_forum'),
    path('ask/', views.ask_question, name='ask_question'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    
     # Consultations
    path('book/<int:expert_id>/', views.book_consultation, name='book_consultation'),
    path('book/', views.book_consultation, name='book_consultation_no_expert'),
    path('payment/<int:consultation_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment/<int:consultation_id>/check/', views.check_payment_status, name='check_payment_status'),
    path('my-consultations/', views.my_consultations, name='my_consultations'),
    path('consultation/<int:pk>/', views.consultation_detail, name='consultation_detail'),
    
    # M-Pesa Callback
    path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),

]