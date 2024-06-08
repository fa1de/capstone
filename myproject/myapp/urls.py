from django.urls import path, include
from .views import GraphView, ProtocolViewSet, ProtocolInfoViewSet, AggregateViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"protocol", ProtocolViewSet)
router.register(r"protocol-info", ProtocolInfoViewSet)
router.register(r"aggregate", AggregateViewSet)

urlpatterns = [
    path(
        "graph/", GraphView.as_view(), name="graph"
    ),  # /myapp/graph/ URL에 graph_view 함수를 매핑합니다.
    path("", include(router.urls)),
]
