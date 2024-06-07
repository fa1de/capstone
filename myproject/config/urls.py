from django.contrib import admin
from django.urls import path, include
from myapp.views import GraphView, UpdateChartView, UpdateChartView, PacketView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graph/', GraphView.as_view(), name='graph'),
    path('api/protocol_counts/', UpdateChartView.as_view(), name='protocol_counts'),
    path('', include('myapp.urls')),
    
]
