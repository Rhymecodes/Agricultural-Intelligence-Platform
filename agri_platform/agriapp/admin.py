from django.contrib import admin
from .models import FarmerProfile, Crop, Pest, WeatherData, CommunityTip
# Register your models here.

admin.site.register(FarmerProfile)
admin.site.register(Crop)
admin.site.register(Pest)
admin.site.register(WeatherData)
admin.site.register(CommunityTip)