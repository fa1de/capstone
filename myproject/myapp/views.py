from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import ProtocolInfo, Protocol, Aggregate
from .serializers import ProtocolInfoSerializer, ProtocolSerializer, AggregateSerializer
from django.db.models import F
from threading import Thread, Event
from .utils.sniffer import get_interfaces, start_sniffer


class GraphView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "graph.html")


class EdgeViewSet(viewsets.ViewSet):
    stop_event = Event()
    sniffer_thread = None

    def list(self, request, *args, **kwargs):
        return JsonResponse({"interfaces": list(get_interfaces())})

    @action(detail=False, methods=["get"])
    def start(self, request, *args, **kwargs):
        interfaces = get_interfaces()
        selected_interface = list(interfaces)[0]
        self.sniffer_thread = Thread(
            target=start_sniffer, args=(selected_interface, self.stop_event)
        )
        self.sniffer_thread.start()

        return HttpResponse("Success to start edge socket thread.")

    @action(detail=False, methods=["get"])
    def stop(self, request, *args, **kwargs):
        self.stop_event.set()
        self.sniffer_thread.join()

        return HttpResponse("Success to stop edge socket thread.")


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
            source_ip = response.data["source_ip"]
            target_ip = response.data["target_ip"]
            ip_key = f"{source_ip}_{target_ip}"
            protocol_name = Protocol.objects.get(id=protocol_id).name

            aggregate, created = Aggregate.objects.get_or_create(
                key=f"protocol-{protocol_name}", defaults={"value": 1}
            )

            if not created:
                # 동시성 문제 방지
                aggregate.value = F("value") + 1
                aggregate.save()

            aggregate, created = Aggregate.objects.get_or_create(
                key=f"ip-{ip_key}", defaults={"value": 1}
            )

            if not created:
                # 동시성 문제 방지
                aggregate.value = F("value") + 1
                aggregate.save()

        return response


class AggregateViewSet(viewsets.ModelViewSet):
    queryset = Aggregate.objects.all()
    serializer_class = AggregateSerializer
