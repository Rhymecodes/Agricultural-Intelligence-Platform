from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from agriapp.models import FarmerProfile, Crop
from .models import Question, Answer, Expert, Consultation, PaymentTransaction
from .forms import QuestionForm, AnswerForm, ConsultationForm
from .mpesa_service import DarajaMpesaService
from django.urls import reverse
import json
import logging

logger = logging.getLogger(__name__)


# Q&A Forum Views
@login_required(login_url='login')
def qa_forum(request):
    """Main Q&A Forum page"""
    try:
        farmer_profile = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('home')
    
    questions = Question.objects.all()
    experts = Expert.objects.filter(is_verified=True)
    
    context = {
        'questions': questions,
        'experts': experts,
        'farmer_profile': farmer_profile,
    }
    
    return render(request, 'consultations/qa_forum.html', context)


@login_required(login_url='login')
def ask_question(request):
    """Post a new question"""
    try:
        farmer_profile = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('home')
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = farmer_profile
            question.save()
            messages.success(request, 'Question posted! Experts will answer soon.')
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm()
    
    context = {'form': form}
    return render(request, 'consultations/ask_question.html', context)


@login_required(login_url='login')
def question_detail(request, pk):
    """View question and answers"""
    question = get_object_or_404(Question, pk=pk)
    question.views += 1
    question.save()
    
    try:
        farmer_profile = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        farmer_profile = None
    
    # Check if user is an expert
    try:
        expert_profile = Expert.objects.get(user=request.user)
    except Expert.DoesNotExist:
        expert_profile = None
    
    if request.method == 'POST' and expert_profile:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = expert_profile
            answer.save()
            messages.success(request, 'Your answer has been posted!')
            return redirect('question_detail', pk=pk)
    else:
        form = AnswerForm() if expert_profile else None
    
    context = {
        'question': question,
        'answers': question.answers.all(),
        'form': form,
        'farmer_profile': farmer_profile,
        'expert_profile': expert_profile,
    }
    
    return render(request, 'consultations/question_detail.html', context)



# Consultation Booking Views
@login_required(login_url='login')
def book_consultation(request, expert_id=None):
    """Book a consultation with expert"""
    try:
        farmer_profile = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('home')
    
    expert = None
    if expert_id:
        expert = get_object_or_404(Expert, id=expert_id)
    
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.farmer = farmer_profile
            consultation.expert = expert if expert else form.cleaned_data.get('expert')
            consultation.amount = consultation.calculate_amount()
            consultation.save()
            
            messages.success(request, 'Consultation booked! Proceeding to payment...')
            return redirect('initiate_payment', consultation_id=consultation.id)
    else:
        form = ConsultationForm()
    
    context = {
        'form': form,
        'expert': expert,
    }
    
    return render(request, 'consultations/book_consultation.html', context)


@login_required(login_url='login')
def initiate_payment(request, consultation_id):
    """Initiate M-Pesa STK Push payment"""
    consultation = get_object_or_404(Consultation, id=consultation_id)
    
    # Verify consultation belongs to logged-in user
    if consultation.farmer.user != request.user:
        messages.error(request, 'Unauthorized access')
        return redirect('qa_forum')
    
    # Don't allow re-payment if already completed
    if consultation.payment_status == 'completed':
        messages.warning(request, 'This consultation has already been paid for.')
        return redirect('consultation_detail', pk=consultation_id)
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        if not phone_number:
            messages.error(request, 'Please enter your phone number')
            return redirect('initiate_payment', consultation_id=consultation_id)
        
        try:
            # Initialize M-Pesa service
            mpesa = DarajaMpesaService()
            
            # Build callback URL
            callback_url = request.build_absolute_uri(reverse('mpesa_callback'))
            
            # Initiate STK Push
            result = mpesa.initiate_stk_push(
                phone_number=phone_number,
                amount=consultation.amount,
                consultation_id=consultation.id,
                description=f"{consultation.topic}",
                callback_url=callback_url
            )
            
            if result['success']:
                # Create/Update payment transaction record
                payment, created = PaymentTransaction.objects.get_or_create(
                    consultation=consultation,
                    defaults={
                        'phone_number': phone_number,
                        'amount': consultation.amount,
                        'transaction_id': result.get('checkout_request_id', ''),
                        'status': 'pending'
                    }
                )
                
                # Update consultation with transaction info
                consultation.mpesa_transaction_id = result.get('checkout_request_id', '')
                consultation.payment_status = 'pending'
                consultation.save()
                
                messages.success(request, 'STK Push sent! Check your phone to enter your M-Pesa PIN.')
                logger.info(f"STK Push initiated for consultation {consultation_id}")
                
                return render(request, 'consultations/payment_waiting.html', {
                    'consultation': consultation,
                    'checkout_request_id': result.get('checkout_request_id'),
                    'merchant_request_id': result.get('merchant_request_id')
                })
            else:
                messages.error(request, f"Payment initiation failed: {result.get('error')}")
                logger.error(f"STK Push failed for consultation {consultation_id}: {result.get('error')}")
                return redirect('initiate_payment', consultation_id=consultation_id)
        
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            logger.error(f"Exception in initiate_payment: {str(e)}")
            return redirect('initiate_payment', consultation_id=consultation_id)
    
    context = {'consultation': consultation}
    return render(request, 'consultations/initiate_payment.html', context)



# M-Pesa Callback Views
@csrf_exempt
@require_http_methods(["POST"])
def mpesa_callback(request):
    """
    Handle M-Pesa payment callback
    This endpoint receives payment status from Safaricom
    """
    try:
        # Parse callback data
        data = json.loads(request.body)
        logger.info(f"M-Pesa Callback received: {data}")
        
        body = data.get('Body', {})
        stk_callback = body.get('stkCallback', {})
        
        checkout_request_id = stk_callback.get('CheckoutRequestID')
        result_code = stk_callback.get('ResultCode')
        result_desc = stk_callback.get('ResultDesc')
        
        # Find consultation and payment by checkout request ID
        try:
            payment = PaymentTransaction.objects.get(transaction_id=checkout_request_id)
            consultation = payment.consultation
        except PaymentTransaction.DoesNotExist:
            logger.warning(f"Payment not found for checkout_request_id: {checkout_request_id}")
            return JsonResponse({'ResultCode': 0, 'ResultDesc': 'OK'})
        
        # Update payment status based on result code
        if result_code == 0:  # Success
            payment.status = 'completed'
            consultation.payment_status = 'completed'
            
            # Extract receipt number if available
            callback_metadata = stk_callback.get('CallbackMetadata', {})
            items = callback_metadata.get('Item', [])
            for item in items:
                if item.get('Name') == 'MpesaReceiptNumber':
                    payment.receipt_number = item.get('Value')
                    consultation.mpesa_receipt_number = item.get('Value')
            
            logger.info(f"Payment {checkout_request_id} completed successfully")
            messages.success = "Payment successful! Your consultation has been confirmed."
        
        else:  # Failed
            payment.status = 'failed'
            consultation.payment_status = 'failed'
            logger.warning(f"Payment {checkout_request_id} failed: {result_desc}")
        
        payment.save()
        consultation.save()
        
        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'OK'})
    
    except Exception as e:
        logger.error(f"Error processing M-Pesa callback: {str(e)}")
        return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Error'}, status=500)


@login_required(login_url='login')
def check_payment_status(request, consultation_id):
    """
    Check payment status via AJAX
    Returns payment status for the consultation
    """
    try:
        consultation = get_object_or_404(Consultation, id=consultation_id)
        
        # Verify ownership
        if consultation.farmer.user != request.user:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        # If payment is completed, redirect to consultation detail
        payment_status = consultation.payment_status
        
        return JsonResponse({
            'success': True,
            'payment_status': payment_status,
            'amount': str(consultation.amount),
            'receipt_number': consultation.mpesa_receipt_number or '',
            'consultation_id': consultation.id
        })
    
    except Exception as e:
        logger.error(f"Error checking payment status: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



# Consultation Management Views
@login_required(login_url='login')
def my_consultations(request):
    """View user's consultations"""
    try:
        farmer_profile = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('home')
    
    consultations = Consultation.objects.filter(farmer=farmer_profile).order_by('-created_at')
    
    context = {'consultations': consultations}
    return render(request, 'consultations/my_consultations.html', context)


@login_required(login_url='login')
def consultation_detail(request, pk):
    """View consultation details"""
    consultation = get_object_or_404(Consultation, pk=pk)
    
    # Check ownership
    if consultation.farmer.user != request.user:
        messages.error(request, 'Unauthorized access')
        return redirect('qa_forum')
    
    context = {'consultation': consultation}
    return render(request, 'consultations/consultation_detail.html', context)