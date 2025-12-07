from django.db import models
from django.contrib.auth.models import User
from agriapp.models import FarmerProfile, Crop

# Create your models here.
class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    farmer_profile = models.OneToOneField(FarmerProfile, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField()
    expertise = models.CharField(max_length=200)  # e.g., "Maize, Beans, Pest Management"
    years_experience = models.IntegerField()
    phone = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)  # In KES
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Expert: {self.user.username}"


class Question(models.Model):
    author = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=300)
    content = models.TextField()
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_solved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(Expert, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-likes', '-created_at']
    
    def __str__(self):
        return f"Answer to: {self.question.title}"


class Consultation(models.Model):
    CONSULTATION_TYPES = [
        ('online', 'Online Consultation'),
        ('physical', 'Physical Office Consultation'),
        ('farm_visit', 'Expert Visiting Farm'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Payment Pending'),
        ('completed', 'Payment Completed'),
        ('failed', 'Payment Failed'),
    ]
    
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='consultations')
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='consultations')
    consultation_type = models.CharField(max_length=20, choices=CONSULTATION_TYPES)
    topic = models.CharField(max_length=200)
    description = models.TextField()
    scheduled_date = models.DateTimeField(null=True, blank=True)
    duration_hours = models.FloatField(default=1.0)  # Duration in hours
    location = models.CharField(max_length=200, blank=True)  # For physical or farm visit
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # In KES
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    mpesa_transaction_id = models.CharField(max_length=100, blank=True)
    mpesa_receipt_number = models.CharField(max_length=100, blank=True)
    
    # Meeting details
    meeting_link = models.URLField(blank=True)  # For online consultations (Zoom, Jitsi, etc.)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.farmer.user.username} - {self.expert.user.username}"
    
    def calculate_amount(self):
        """Calculate consultation amount based on type and duration"""
        return self.expert.hourly_rate * self.duration_hours


class PaymentTransaction(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE, related_name='payment')
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    receipt_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment: {self.transaction_id}"
    