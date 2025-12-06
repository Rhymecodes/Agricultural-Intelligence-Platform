from django.contrib import admin
from .models import Plant, Pest, Disease

# Register your models here.
admin.site.register(Plant)
admin.site.register(Pest)
admin.site.register(Disease)