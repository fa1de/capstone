from django.shortcuts import render
from django.http import JsonResponse
import json
from rest_framework import viewsets
from .models import ProtocolInfo, Protocol
from rest_framework.views import APIView
from .serializers import ProtocolInfoSerializer, ProtocolSerializer


# View 정의
class GraphView(APIView):
    def get(self, request):
        return render(request, "graph.html")


class UpdateChartView(APIView):
    protocol_info = {
        "TCP": 0,
        "UDP": 0,
        "ICMP": 0,
        "HTTP": 0,
        "FTP": 0,
        "DNS": 0,
        "SSH": 0,
    }

    @classmethod
    def update_protocol_counts(cls, protocol_name):
        if protocol_name in cls.protocol_info:
            cls.protocol_info[protocol_name] += 1

    def get(self, request):
        return JsonResponse(
            self.protocol_info
        )  # 수정: {'protocol_counts': self.protocol_info} -> self.protocol_info

    def post(self, request):
        try:
            data = request.data
            protocol_name = list(data.keys())[0]
            count = data[protocol_name]
            self.update_protocol_counts(protocol_name)
            return JsonResponse(
                {"success": True, "protocol_counts": self.protocol_info}
            )
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)


class ProtocolViewSet(viewsets.ModelViewSet):
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer


class ProtocolInfoViewSet(viewsets.ModelViewSet):
    queryset = ProtocolInfo.objects.all()
    serializer_class = ProtocolInfoSerializer
