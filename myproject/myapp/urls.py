from django.urls import path, include
from .views import (
    SniffViewSet,
    GraphView,
    ProtocolViewSet,
    ProtocolViewSet,
    AggregateViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"protocol", ProtocolViewSet)
router.register(r"aggregate", AggregateViewSet)
router.register(r"sniff", SniffViewSet, basename="sniff")

urlpatterns = [
    path("graph/", GraphView.as_view(), name="graph"),
    path("", include(router.urls)),
]
