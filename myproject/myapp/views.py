from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
from rest_framework import viewsets, serializers
from myapp.serializers import PacketSerializer
from myapp.models import ProtocolInfo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# View 정의
class GraphView(APIView):
    def get(self, request):
        protocols = ["TCP", "UDP", "ICMP", "HTTP", "FTP", "DNS", "SSH"]
        return render(request, "graph.html", {"protocols": protocols})


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
    
    def main_view(request):
        # 뷰의 로직
        return render(request, 'main.html')
       


class PacketView(viewsets.ModelViewSet):
    queryset = ProtocolInfo.objects.all()
    serializer_class = PacketSerializer
