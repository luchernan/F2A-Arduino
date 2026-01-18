# backend/authiot/admin.py
from django.contrib import admin
from .models import CardUser

admin.site.register(CardUser)
