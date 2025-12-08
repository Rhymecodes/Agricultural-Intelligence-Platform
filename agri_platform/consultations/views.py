from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Question, ConsultationBooking, Consultation,PaymentTransaction, Expert
from datetime import date
import requests
from requests.auth import HTTPBasicAuth
import base64
import datetime
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
import time
from django.utils import timezone
from agriapp.models import FarmerProfile

@login_required
def consultations_home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'consultations/consultations.html', {'questions': questions})


@login_required
def ask_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question')
        if question_text:
            # Save the question
            Question.objects.create(
                user=request.user,
                question=question_text
            )
            messages.success(request, "Your question has been submitted!")
            return redirect('qa_forum')  # redirect to the forum page
        else:
            messages.error(request, "Please enter a question.")
    
    return render(request, 'consultations/ask.html')

@login_required(login_url='login')
def qa_forum(request):
    try:
        farmer_profile = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('home')
    
    questions = Question.objects.all()  # ← This line gets all questions
    experts = Expert.objects.filter(is_verified=True)
    
    return render(request, 'consultations/qa_forum.html', {
        'questions': questions,  # ← Pass questions to template
        'experts': experts,
        'farmer_profile': farmer_profile,
    })

@login_required
def book_consultation(request):
    booking = None   # to show mpesa section only after booking

    # Booking submission
    if request.method == 'POST' and "create_booking" in request.POST:
        c_type = request.POST.get('consultation_type')
        phone = request.POST.get('phone')
        preferred_date = request.POST.get('date')

        # Pricing
        prices = {
            'online': 500,
            'office': 1500,
            'farm': 3000,
        }
        amount = prices.get(c_type, 0)

        booking = ConsultationBooking.objects.create(
            user=request.user,
            consultation_type=c_type,
            phone_number=phone,
            preferred_date=preferred_date,
            amount=amount
        )

        messages.success(request, "Booking created. Proceed with payment.")

    # Payment submission
    if request.method == 'POST' and "pay_now" in request.POST:
        booking_id = request.POST.get("booking_id")
        booking = ConsultationBooking.objects.get(id=booking_id)
        phone = booking.phone_number
        amount = booking.amount

        # Create transaction
        transaction = PaymentTransaction.objects.create(
            consultation=booking,
            phone_number=phone,
            amount=amount,
            status='pending'
        )

        # Send STK
        response = lipa_na_mpesa(phone, amount)

        if "CheckoutRequestID" in response:
            transaction.checkout_request_id = response["CheckoutRequestID"]
            transaction.save()

        if response.get('ResponseCode') == '0':
            messages.success(request, 'STK Push sent! Check your phone.')
        else:
            messages.error(request, f"Error: {response.get('errorMessage')}")

    return render(request, 'consultations/book_and_pay.html', {"booking": booking})



@login_required
def mpesa_payment(request, consultation_id):
    # Use booking instead of consultation
    booking = ConsultationBooking.objects.get(id=consultation_id)

    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = booking.amount  # get amount from booking

        # 1. Create a payment record BEFORE sending STK
        transaction = PaymentTransaction.objects.create(
            consultation=booking,  #  use booking
            phone_number=phone,
            amount=amount,
            status='pending'
        )

        # 2. Trigger STK
        response = lipa_na_mpesa(phone, amount)

        # 3. Save CheckoutRequestID to map callback to this record
        if "CheckoutRequestID" in response:
            transaction.checkout_request_id = response["CheckoutRequestID"]
            transaction.save()

        if response.get('ResponseCode') == '0':
            messages.success(request, 'STK Push sent! Check your phone to complete payment.')
        else:
            messages.error(request, f"Error: {response.get('errorMessage')}")

    return render(request, 'consultations/mpesa.html', {"booking": booking})  # ✅ pass booking



def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    token = response.json().get('access_token')
    return token

def lipa_na_mpesa(phone_number, amount):
    access_token = get_access_token()  # make sure this function uses MPESA_CONSUMER_KEY & SECRET
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    password_str = settings.MPESA_EXPRESS_SHORTCODE + settings.MPESA_PASSKEY + timestamp
    password = base64.b64encode(password_str.encode()).decode('utf-8')

    stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}

    payload = {
        "BusinessShortCode": settings.MPESA_EXPRESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_EXPRESS_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "Consultation",
        "TransactionDesc": "Consultation Payment"
    }

    response = requests.post(stk_url, json=payload, headers=headers)
    return response.json()


@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        callback = data['Body']['stkCallback']
        checkout_request_id = callback['CheckoutRequestID']
        result_code = callback['ResultCode']

        # Find the matching transaction
        try:
            transaction = PaymentTransaction.objects.get(
                checkout_request_id=checkout_request_id
            )
        except PaymentTransaction.DoesNotExist:
            return HttpResponse("Transaction not found", status=404)

        if result_code == 0:
            # Paid successfully
            items = callback["CallbackMetadata"]["Item"]
            amount = items[0]["Value"]
            receipt = items[1]["Value"]

            transaction.status = "success"
            transaction.mpesa_receipt = receipt
            transaction.amount = amount
            transaction.save()

            # Mark consultation as paid
            booking = transaction.consultation   # <-- this is ConsultationBooking
            booking.is_paid = True
            booking.mpesa_receipt = receipt
            booking.save()

        else:
            transaction.status = "failed"
            transaction.save()

        return HttpResponse("OK", status=200)

    return HttpResponse("Invalid request", status=400)

def notify_user(consultation):
    send_mail(
        subject='Your Consultation is Answered',
        message=f'Your question: {consultation.question}\nAnswer: {consultation.answer}',
        from_email='no-reply@example.com',
        recipient_list=[consultation.user.email],
        fail_silently=True,
    )
