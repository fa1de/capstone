from django.shortcuts import render
from django.http import JsonResponse
import json
from rest_framework import viewsets
from .models import ProtocolInfo, Protocol, Aggregate
from rest_framework.views import APIView
from .serializers import ProtocolInfoSerializer, ProtocolSerializer, AggregateSerializer
from rest_framework import status
from django.db.models import F


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

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            print(response.data)
            protocol_id = response.data["protocol_id"]
            protocol_name = Protocol.objects.get(id=protocol_id).name
            aggregate, created = Aggregate.objects.get_or_create(
                key=f"{protocol_name}", defaults={"value": 0}
            )
            # orm으로 값을 증가시키면 동시성 문제가 발생할 수 있기 때문에
            # F()를 사용하여 데이터베이스에서 직접 값을 증가시킵니다.
            aggregate.value = F("value") + 1
            aggregate.save()

        return response


class AggregateViewSet(viewsets.ModelViewSet):
    queryset = Aggregate.objects.all()
    serializer_class = AggregateSerializer
