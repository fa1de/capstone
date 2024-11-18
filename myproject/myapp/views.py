from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import Protocol, Protocol, Aggregate
from .serializers import ProtocolInfoSerializer, AggregateSerializer
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
import json
from threading import Thread, Event
from .utils.sniffer import get_interfaces, start_sniffer
from django.shortcuts import redirect
import os
from django.conf import settings
import ast


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

    @action(detail=False, methods=["delete"])
    def delete_all(self, request, *args, **kwargs):
        try:
            Protocol.objects.all().delete()
            return JsonResponse(
                {"message": "Success to delete all protocols."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@csrf_exempt  # CSRF 토큰 검사를 비활성화 (테스트 환경에서 사용 권장)
def save_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code")

            # 코드 문법 검사 (간단한 예: ast 모듈을 사용해 구문 오류를 체크)
            try:
                ast.parse(code)  # Python 코드의 문법이 유효한지 검사
            except SyntaxError as e:
                # 문법 오류 메시지와 라인 번호를 반환
                return JsonResponse(
                    {"message": f"문법 오류: {e.msg} at line {e.lineno}"}, status=400
                )

            try:
                exec(code, {})  # 코드 실행해서 오류를 발생시킬 수 있는지 검사
            except Exception as e:
                return JsonResponse({"message": f"실행 오류: {str(e)}"}, status=400)

            # rules.py 파일 경로
            file_path = os.path.join(settings.BASE_DIR, "myapp", "utils", "rules.py")

            # rules.py 파일을 덮어쓰는 방식으로 열기
            with open(file_path, "w") as file:
                file.write(code)  # 새로운 코드로 덮어쓰기

            return JsonResponse(
                {"message": "저장되었습니다.", "code": code}, status=200
            )  # 저장된 코드도 반환

        except Exception as e:
            return JsonResponse(
                {"message": "오류로 인해 저장되지 않았습니다.", "error": str(e)},
                status=500,
            )

    return JsonResponse({"message": "Invalid request"}, status=400)


def main(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, "myapp", "utils", "rules.py")

        # rules.py 파일을 읽어와서 code에 전달
        with open(file_path, "r") as file:
            code = file.read()

        return render(request, "main.html", {"code": code})

    except Exception as e:
        return JsonResponse(
            {"message": "파일을 읽을 수 없습니다.", "error": str(e)}, status=500
        )


class AggregateViewSet(viewsets.ModelViewSet):
    queryset = Aggregate.objects.all()
    serializer_class = AggregateSerializer

    @action(detail=False, methods=["delete"])
    def delete_all(self, request, *args, **kwargs):
        try:
            Aggregate.objects.all().delete()
            return JsonResponse(
                {"message": "Success to delete all protocols."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def login(request):
    return render(request, "login.html")


def regex(request):
    return render(request, "regex.html")


def save_regex(request):
    if request.method == "POST":
        name = request.POST.get("name")
        pattern = request.POST.get("pattern")
        # 여기에 정규 표현식을 저장하는 로직 추가
        return redirect("main_page")  # 메인 페이지로 리다이렉션


def test_regex(request):
    # 정규 표현식을 테스트하는 로직을 여기에 추가
    return HttpResponse("Testing regular expression.")  # 임시 응답
