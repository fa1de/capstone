from django.db import models


class Aggregate(models.Model):
    key = models.CharField()
    value = models.IntegerField()

    def __str__(self) -> str:
        return str(self.key)


class Protocol(models.Model):
    name = models.CharField(max_length=5, default=False)

    def __str__(self):
        return self.name


class ProtocolInfo(models.Model):
    protocol_id = models.ForeignKey(
        Protocol, on_delete=models.CASCADE, related_name="protocols"
    )
    source_ip = models.CharField(max_length=20, default=False)
    target_ip = models.CharField(max_length=20, default=False)

    def __str__(self):
        return self.source_ip
