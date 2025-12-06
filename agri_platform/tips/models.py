from django.db import models
from django.contrib.auth.models import User
from agriapp.models import FarmerProfile

# Create your models here.
class Tip(models.Model):
    author = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    explanation = models.TextField()
    image = models.ImageField(upload_to='tips/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tip')

    def __str__(self):
        return f"{self.user.username} likes {self.tip.title}"


class Comment(models.Model):
    author = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE)
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.user.username} on {self.tip.title}"
