from django.db import models
from django.utils import timezone

# Create your models here.

class Member(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    status=models.CharField(max_length=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name