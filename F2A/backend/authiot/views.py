# backend/authiot/views.py
from django.shortcuts import render, redirect
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
            if card.name in ["AZUL", "BLANCO"]:
                status = "OK"
                message = f"Bienvenido {card.name}"
            
        except CardUser.DoesNotExist:
            pass
        
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
        # Buscamos cualquier intento reciente (hace menos de 3 segundos)
        time_threshold = timezone.now() - timedelta(seconds=3)
        latest_log = AccessLog.objects.filter(
            timestamp__gte=time_threshold
        ).order_by('-timestamp').first()

        if latest_log:
            if latest_log.status == "OK":
                # Sesión para éxito
                request.session['auth_user_name'] = latest_log.user_name
                request.session['is_authenticated_iot'] = True
                return Response({
                    "found": True, 
                    "status": "OK",
                    "user_name": latest_log.user_name
                })
            else:
                # Informamos del fallo
                return Response({
                    "found": True, 
                    "status": "DENY"
                })
        
        return Response({"found": False})

def index_view(request):
    # Al volver al inicio, podemos limpiar la sesión para obligar a pasar la tarjeta de nuevo
    if 'is_authenticated_iot' in request.session:
        del request.session['is_authenticated_iot']
    return render(request, 'authiot/index.html')

def dashboard_view(request):
    # VALIDACIÓN REAL: Si no hay sesión de IoT, fuera.
    if not request.session.get('is_authenticated_iot'):
        return redirect('/')
    
    user_name = request.session.get('auth_user_name', 'Usuario')
    return render(request, 'authiot/dashboard.html', {'user_name': user_name})
