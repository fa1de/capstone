from django.urls import path, include
from .views import GraphView, UpdateChartView
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'packet', views.PacketView, basename='packet')  # URL에는 소문자 및 하이픈을 사용하고 모델 이름과 일치하도록 설정합니다.

urlpatterns = [
    path('graph/', GraphView.as_view(), name='graph'),  # /myapp/graph/ URL에 graph_view 함수를 매핑합니다.   
    path('protocol-count/', UpdateChartView.as_view(), name='protocol-count'),  # 프로토콜 카운트 뷰에 대한 URL 패턴
    path('', include(router.urls)),
]