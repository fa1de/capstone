from rest_framework import serializers
from .models import ProtocolInfo
from rest_framework.response import Response
from rest_framework.views import APIView


class PacketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolInfo
        fields = ["protocol_name", "count"]
