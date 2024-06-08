from django.contrib import admin

from .models import Aggregate, ProtocolInfo, Protocol


# Register your models here.
admin.site.register(ProtocolInfo)
admin.site.register(Protocol)
admin.site.register(Aggregate)
