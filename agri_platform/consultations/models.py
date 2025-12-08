from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Expert(models.Model):
    # If you prefer to allow experts not linked to a user, change to null=True
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='expert_profile')
    title = models.CharField(max_length=100, blank=True)  # e.g., "Agronomist"
    specialization = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.specialization})"

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    answered_by = models.ForeignKey(Expert, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:50]


class ConsultationBooking(models.Model):
    CONSULTATION_TYPES = [
        ('online', 'Online Consultation'),
        ('office', 'Office Visit'),
        ('farm', 'Farm Visit'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    consultation_type = models.CharField(max_length=20, choices=CONSULTATION_TYPES)
    phone_number = models.CharField(max_length=15)
    preferred_date = models.DateField()

    amount = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    mpesa_receipt = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.consultation_type}"

class Consultation(models.Model):
    # existing fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    mpesa_receipt = models.CharField(max_length=50, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    # If your flow connects Answers to Question model (not Consultation),
    # adjust the FK below to point to your Question model.
    # I'm assuming you have a Question model already.
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    expert = models.ForeignKey(Expert, on_delete=models.SET_NULL, null=True, blank=True, related_name='answers')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)  # admin/asker may mark accepted

    def __str__(self):
        return f"Answer by {self.expert or 'Unknown'} on {self.created_at:%Y-%m-%d}"


class PaymentTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    consultation = models.ForeignKey('ConsultationBooking', on_delete=models.CASCADE, related_name='transactions')
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    mpesa_receipt = models.CharField(max_length=100, blank=True, null=True)

    # store daraja raw payload optionally
    callback_body = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TX {self.id} - {self.phone_number} - {self.status}"
    
