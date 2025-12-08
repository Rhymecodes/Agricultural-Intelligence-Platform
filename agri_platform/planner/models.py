from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FarmTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField()

    TASK_TYPES = [
        ('planting', 'Planting'),
        ('watering', 'Watering'),
        ('fertilizing', 'Fertilizing'),
        ('harvesting', 'Harvesting'),
    ]
    task_type = models.CharField(max_length=20, choices=TASK_TYPES, default='planting')

    def __str__(self):
        return self.title