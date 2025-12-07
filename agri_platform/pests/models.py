from django.db import models

# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='plants/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Pest(models.Model):
    name = models.CharField(max_length=100)
    symptoms = models.TextField()
    treatment = models.TextField()
    image = models.ImageField(upload_to="pests/", blank=True, null=True)

    plants = models.ManyToManyField("Plant", related_name="pests")

    def __str__(self):
        return self.name
    
class Disease(models.Model):
    name = models.CharField(max_length=100)
    cause = models.TextField()
    symptoms = models.TextField()
    treatment = models.TextField()
    image = models.ImageField(upload_to="diseases/", blank=True, null=True)

    plants = models.ManyToManyField("Plant", related_name="diseases")

    def __str__(self):
        return self.name