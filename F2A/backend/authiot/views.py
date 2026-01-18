# backend/authiot/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CardUser, AccessLog
from django.utils import timezone
from datetime import timedelta

class RFIDValidateView(APIView):

    def post(self, request):
        uid = request.data.get("uid")
        status = "DENY"
        message = "UID no autorizado"
        user_name = "Desconocido"

        try:
            card = CardUser.objects.get(uid=uid)
            user_name = card.name
            # Check for authorized names specifically as per original logic
            if card.name in ["AZUL", "BLANCO"]:
                status = "OK"
                message = f"Bienvenido {card.name}"
            
        except CardUser.DoesNotExist:
            pass
        
        # Log the attempt
        AccessLog.objects.create(
            uid=uid, 
            user_name=user_name, 
            status=status
        )

        if status == "OK":
            return Response({"status": "OK", "message": message})
        else:
            return Response({"status": "DENY", "message": message}, status=403)

class CheckAccessView(APIView):
    def get(self, request):
        # Check for successful logins in the last 5 seconds
        time_threshold = timezone.now() - timedelta(seconds=5)
        # We want the LATEST success
        latest_log = AccessLog.objects.filter(
            timestamp__gte=time_threshold,
            status="OK"
        ).order_by('-timestamp').first()

        if latest_log:
            return Response({
                "found": True, 
                "user_name": latest_log.user_name,
                "timestamp": str(latest_log.timestamp)
            })
        return Response({"found": False})

def index_view(request):
    return render(request, 'authiot/index.html')

def dashboard_view(request):
    user_name = request.GET.get('user', 'Usuario')
    return render(request, 'authiot/dashboard.html', {'user_name': user_name})
