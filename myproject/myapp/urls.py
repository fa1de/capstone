from django.urls import path, include
from .views import (
    EdgeViewSet,
    GraphView,
    ProtocolViewSet,
    ProtocolInfoViewSet,
    AggregateViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"protocol", ProtocolViewSet)
router.register(r"protocol-info", ProtocolInfoViewSet)
router.register(r"aggregate", AggregateViewSet)
router.register(r"edge", EdgeViewSet, basename="edge")

urlpatterns = [
    path("graph/", GraphView.as_view(), name="graph"),
    path("", include(router.urls)),
]
