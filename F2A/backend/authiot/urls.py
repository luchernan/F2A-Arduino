# backend/authiot/urls.py
from django.urls import path
from .views import RFIDValidateView, CheckAccessView

urlpatterns = [
    path('rfid/validate/', RFIDValidateView.as_view()),
    path('check-access/', CheckAccessView.as_view()),
]
