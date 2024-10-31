from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import Protocol, Protocol, Aggregate
from .serializers import ProtocolInfoSerializer, AggregateSerializer
from django.db.models import F
from threading import Thread, Event
from .utils.sniffer import get_interfaces, start_sniffer


class GraphView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "graph.html")


class SniffViewSet(viewsets.ViewSet):
    stop_event = Event()
    sniffer_thread = None

    def list(self, request, *args, **kwargs):
        return JsonResponse({"interfaces": list(get_interfaces())})

    @action(detail=False, methods=["get"])
    def start(self, request, *args, **kwargs):
        interfaces = get_interfaces()
        interface = int(
            request.query_params.get("i", -1)
        )  # Default to 0 if not provided

        if interface == -1:
            raise ValueError("Invalid interface index")

        selected_interface = list(interfaces)[interface]
        self.sniffer_thread = Thread(
            target=start_sniffer, args=(selected_interface, self.stop_event)
        )
        self.sniffer_thread.start()

        return JsonResponse({"msg": "Success to start sniff socket thread."})

    @action(detail=False, methods=["get"])
    def stop(self, request, *args, **kwargs):
        self.stop_event.set()
        if not self.sniffer_thread:
            raise ValueError("Sniffer thread is not running")
        self.sniffer_thread.join()
        self.sniffer_thread = None

        return JsonResponse("Success to stop sniff socket thread.")


def save_aggregate(key):
    aggregate, created = Aggregate.objects.get_or_create(key=key, defaults={"value": 1})
    if not created:
        # 동시성 문제 방지
        aggregate.value = F("value") + 1
        aggregate.save()


class ProtocolViewSet(viewsets.ModelViewSet):
    queryset = Protocol.objects.all()
    serializer_class = ProtocolInfoSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            print(response.data)
            protocol_name = response.data["protocol_name"]
            source_ip = response.data["source_ip"]
            target_ip = response.data["target_ip"]
            pattern = response.data["pattern"]

            save_aggregate(f"protocol<|start|>{protocol_name}")
            save_aggregate(f"ip<|start|>{source_ip}_{target_ip}")
            save_aggregate(f"pattern<|start|>{protocol_name}-{pattern}")

        return response


class AggregateViewSet(viewsets.ModelViewSet):
    queryset = Aggregate.objects.all()
    serializer_class = AggregateSerializer

def login(request):
    return render(request, 'login.html')

def main(request):
    return render(request, 'main.html')

def save_regex(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        pattern = request.POST.get('pattern')
        # 여기에 정규 표현식을 저장하는 로직 추가
        return redirect('main_page')  # 메인 페이지로 리다이렉션

def test_regex(request):
    # 정규 표현식을 테스트하는 로직을 여기에 추가
    return HttpResponse("Testing regular expression.")  # 임시 응답