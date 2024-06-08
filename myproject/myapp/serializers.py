from rest_framework import serializers
from .models import Protocol, ProtocolInfo


class ProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        fields = "__all__"


class ProtocolInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolInfo
        fields = "__all__"
