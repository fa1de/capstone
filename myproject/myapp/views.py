from django.shortcuts import render
from django.http import JsonResponse
import json
from rest_framework import viewsets
from myapp.serializers import ProtocolInfoSerializer
from myapp.models import ProtocolInfo
from rest_framework.views import APIView
from .serializers import ProtocolInfoSerializer
from rest_framework.decorators import action


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


class ProtocolInfoViewSet(viewsets.ModelViewSet):
    queryset = ProtocolInfo.objects.all()
    serializer_class = ProtocolInfoSerializer

    # 커스텀 엔드포인트 예제: 가장 최근에 출판된 책을 가져오는 엔드포인트
    @action(detail=False, methods=["get"])
    def graph(self, request):
        protocols = ["TCP", "UDP", "ICMP", "HTTP", "FTP", "DNS", "SSH"]
        return render(request, "graph.html", {"protocols": protocols})
