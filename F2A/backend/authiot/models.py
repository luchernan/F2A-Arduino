# backend/authiot/models.py
from django.db import models

class CardUser(models.Model):
    uid = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.uid})"
class AccessLog(models.Model):
    user_name = models.CharField(max_length=50)
    uid = models.CharField(max_length=32)
    status = models.CharField(max_length=10) # "OK" or "DENY"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user_name} ({self.status})"
