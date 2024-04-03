# model.py
from django.db import models

class PacketLog(models.Model):
    packet_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# view.py
from django.http import JsonResponse
from .models import PacketLog

def receive_packet(request):
    if request.method == 'POST':
        packet_data = request.body.decode('utf-8')
        PacketLog.objects.create(packet_data=packet_data)
        return JsonResponse({'message': 'Packet received successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
