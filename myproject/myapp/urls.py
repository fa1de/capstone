from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"protocol", ProtocolViewSet)
router.register(r"protocol-info", ProtocolInfoViewSet)

urlpatterns = [
    path(
        "graph/", GraphView.as_view(), name="graph"
    ),  # /myapp/graph/ URL에 graph_view 함수를 매핑합니다.
    path(
        "protocol-count/", UpdateChartView.as_view(), name="protocol-count"
    ),  # 프로토콜 카운트 뷰에 대한 URL 패턴
    path("", include(router.urls)),
]
