from django import forms
from agriapp.models import FarmerProfile, Crop, Pest, WeatherData
from tips.models import Tip
from planner.models import FarmTask
from consultations.models import ConsultationBooking, Consultation
from pests.models import Plant, Pest, Disease
class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ['user', 'phone', 'location', 'farm_size']


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'description', 'image']


class PestForm(forms.ModelForm):
    class Meta:
        model = Pest
        fields = ['name', 'symptoms', 'image', 'treatment', 'plants']

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ['name', 'cause', 'symptoms','treatment','image','plants']
        
class WeatherDataForm(forms.ModelForm):
    class Meta:
        model = WeatherData
        fields = ['location', 'date', 'temperature', 'humidity', 'rainfall']


class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['author', 'title', 'explanation', 'image']


class FarmTaskForm(forms.ModelForm):
    class Meta:
        model = FarmTask
        fields = ['user', 'title', 'date', 'task_type']


class ConsultationBookingForm(forms.ModelForm):
    class Meta:
        model = ConsultationBooking
        fields = ['user', 'consultation_type', 'phone_number', 'preferred_date', 'amount', 'is_paid', 'mpesa_receipt']

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['user', 'question', 'is_paid', 'mpesa_receipt', 'amount_paid', 'phone']