from django.contrib import admin
from .models import Expert, Question, Answer, Consultation, PaymentTransaction

# Register your models here.

admin.site.register(Expert)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Consultation)
admin.site.register(PaymentTransaction)