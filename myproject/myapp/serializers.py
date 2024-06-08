from rest_framework import serializers
from .models import ProtocolInfo


class ProtocolInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolInfo
        fields = "__all__"
