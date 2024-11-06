from django.db import models


class Aggregate(models.Model):
    key = models.CharField()
    value = models.IntegerField()

    def __str__(self) -> str:
        return str(self.key)


class Protocol(models.Model):
    protocol_name = models.CharField(max_length=20, default=False)
    source_ip = models.CharField(max_length=20, default=False)
    target_ip = models.CharField(max_length=20, default=False)
    pattern = models.CharField(default="")

    def __str__(self):
        return self.source_ip
