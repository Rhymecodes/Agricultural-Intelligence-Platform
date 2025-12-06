from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100)
    farm_size = models.FloatField(default=0)
    
    def __str__(self):
        return self.user.username
    
# Crop
class Crop(models.Model):
    name = models.CharField(max_length=100)
    planting_month = models.IntegerField()
    harvest_month = models.IntegerField()
    days_to_maturity = models.IntegerField()
    water_needs = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

# Pest
class Pest(models.Model):
    name = models.CharField(max_length=100)
    symptoms = models.TextField()
    prevention = models.TextField()
    treatment = models.TextField()
    
    def __str__(self):
        return self.name

# Weather Data
class WeatherData(models.Model):
    location = models.CharField(max_length=100)
    date = models.DateField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()
    
    def __str__(self):
        return f"{self.location} - {self.date}"

# Community Tips
class CommunityTip(models.Model):
    author = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title