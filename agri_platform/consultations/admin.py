from django.contrib import admin
from .models import Expert, Question, Answer, Consultation, PaymentTransaction

# Register your models here.

admin.site.register(Expert)
admin.site.register(Question)
admin.site.register(Answer)

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__username', 'question')

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'phone_number', 'amount', 'status', 'mpesa_receipt')
    list_filter = ('status',)
    search_fields = ('mpesa_receipt', 'phone_number')