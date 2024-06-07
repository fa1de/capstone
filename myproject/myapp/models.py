from django.db import models

class ProtocolInfo(models.Model):
    protocol_name = models.CharField(max_length=5, default=False)
    src_IP = models.CharField(max_length=20, default=False)
    dest_IP = models.CharField(max_length=20, default=False)
    count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.protocol_name
    
