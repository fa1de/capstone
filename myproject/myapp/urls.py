from django.urls import path, include
from .views import (
    SniffViewSet,
    GraphView,
    ProtocolViewSet,
    ProtocolViewSet,
    AggregateViewSet,
    login,
    main,
    save_regex
)
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"protocol", ProtocolViewSet)
router.register(r"aggregate", AggregateViewSet)
router.register(
    r"sniff", SniffViewSet, basename="sniffmyproject/static/images/favicon.ico"
)

urlpatterns = [
    path("graph/", GraphView.as_view(), name="graph"),
    path("", include(router.urls)),
    path("login/", view=login, name="login"),
    path("main/", views.main, name="main"),
    path('main/', views.main, name='main_page'),
    path('save-regex/', views.save_regex, name='save_regex'),  # 정규 표현식 저장 URL
    path('test-regex/', views.test_regex, name='test_regex'),  # 정규 표현식 테스트 URL
]
