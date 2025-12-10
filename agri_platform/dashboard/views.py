from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Sum
from django.contrib import messages
from datetime import date
from agriapp.models import FarmerProfile, Crop, Pest, WeatherData, CommunityTip
from tips.models import Tip
from planner.models import FarmTask
from consultations.models import ConsultationBooking, PaymentTransaction, Consultation
from .forms import (FarmerProfileForm, PlantForm, PestForm,
WeatherDataForm, TipForm, FarmTaskForm)
from pests.models import Plant, Pest

#Dashboard Home
def dashboard_home(request):
    context = {
       'farmers_count': FarmerProfile.objects.count(),
        'plants_count': Plant.objects.count(),
        'pests_count': Pest.objects.count(),
        'tips_count': Tip.objects.count(),
        'consultations_count': ConsultationBooking.objects.count(),
        'pending_payments_count': ConsultationBooking.objects.filter(is_paid=False).count(),
        'payment_txs_pending': PaymentTransaction.objects.filter(status='pending').count(),
        'total_revenue': PaymentTransaction.objects.filter(status='success').aggregate(total=Sum('amount'))['total'] or 0,
        'today_tasks_count': FarmTask.objects.filter(date=date.today()).count(),
}
    return render(request, 'dashboard/dashboard_home.html', context)

#  Generic confirm delete (fallback) 
def confirm_delete(request):
    return render(request, 'dashboard/confirm_delete.html', {})

#  Farmers CRUD 
def farmers_list(request):
    farmers = FarmerProfile.objects.select_related('user').all().order_by('-id')
    return render(request, 'dashboard/farmers_list.html', {'farmers': farmers})


def farmer_create(request):
    if request.method == 'POST':
        form = FarmerProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farmer profile created')
            return redirect('dashboard:farmers_list')
    else:
        form = FarmerProfileForm()
        return render(request, 'dashboard/farmers_form.html', {'form': form})


def farmer_edit(request, pk):
    farmer = get_object_or_404(FarmerProfile, pk=pk)
    if request.method == 'POST':
        form = FarmerProfileForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farmer profile updated')
            return redirect('dashboard:farmers_list')
    else:
        form = FarmerProfileForm(instance=farmer)
        return render(request, 'dashboard/farmers_form.html', {'form': form, 'farmer': farmer})


def farmer_delete(request, pk):
    farmer = get_object_or_404(FarmerProfile, pk=pk)
    if request.method == 'POST':
        farmer.delete()
        messages.success(request, 'Farmer profile deleted')
        return redirect('dashboard:farmers_list')
    return render(request, 'dashboard/confirm_delete.html', {'obj': farmer})

#  Crops CRUD 
def plant_list(request):
    # Fetch all plants from the database
    plants = Plant.objects.all().order_by('id')  # optional: sort by id
    context = {
        'plants': plants
    }
    return render(request, 'dashboard/plant_list.html', context)

def plant_create(request):
    if request.method == 'POST':
        form = PlantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'plant added')
            return redirect('dashboard:plant_list')
    else:
        form = PlantForm()
        return render(request, 'dashboard/plant_form.html', {'form': form})


def plant_edit(request, pk):
    # Example edit view placeholder
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == 'POST':
        # handle form submission
        pass
    return render(request, 'dashboard/plants_form.html', {'plant': plant})


def plant_delete(request, pk):
    plant = get_object_or_404(plant, pk=pk)
    if request.method == 'POST':
        plant.delete()
        messages.success(request, 'Plant deleted')
        return redirect('dashboard:plant_list')
    return render(request, 'dashboard/confirm_delete.html', {'obj': plant})

#  Pests CRUD 
def pests_list(request):
    pests = Pest.objects.all().order_by('name')
    return render(request, 'dashboard/pests_list.html', {'pests': pests})


def pest_create(request):
    if request.method == 'POST':
        form = PestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pest added')
            return redirect('dashboard:pests_list')
    else:
        form = PestForm()
        return render(request, 'dashboard/pests_form.html', {'form': form})


def pest_edit(request, pk):
    pest = get_object_or_404(Pest, pk=pk)
    if request.method == 'POST':
        form = PestForm(request.POST, instance=pest)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pest updated')
            return redirect('dashboard:pests_list')
    else:
        form = PestForm(instance=pest)
        return render(request, 'dashboard/pests_form.html', {'form': form, 'pest': pest})


def pest_delete(request, pk):
    pest = get_object_or_404(Pest, pk=pk)
    if request.method == 'POST':
        pest.delete()
        messages.success(request, 'Pest deleted')
        return redirect('dashboard:pests_list')
    return render(request, 'dashboard/confirm_delete.html', {'obj': pest})


#  Tips (read / delete) 
def tips_list(request):
    tips = Tip.objects.select_related('author').all().order_by('-created_at')
    return render(request, 'dashboard/tips_list.html', {'tips': tips})


def tip_delete(request, pk):
    tip = get_object_or_404(Tip, pk=pk)
    if request.method == 'POST':
        tip.delete()
        messages.success(request, 'Tip deleted')
        return redirect('dashboard:Tips_list')
    return render(request, 'dashboard/tips_list.html', {'tips': tips})

#  Consultations & Payments 
def consultations_list(request):
    bookings = ConsultationBooking.objects.select_related('user').order_by('-created_at')
    return render(request, 'dashboard/consultations_list.html', {'bookings': bookings})

def payments_list(request):
    txs = PaymentTransaction.objects.select_related('consultation').order_by('-created_at')
    total_revenue = PaymentTransaction.objects.filter(status='success').aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'dashboard/payments_list.html', {'txs': txs, 'total_revenue': total_revenue})


