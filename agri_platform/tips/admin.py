from django.contrib import admin
from .models import Tip, Like, Comment

# Register your models here.
admin.site.register(Tip)
admin.site.register(Like)
admin.site.register(Comment)