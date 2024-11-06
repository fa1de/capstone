from django.contrib import admin

from .models import Aggregate, Protocol


# Register your models here.
admin.site.register(Protocol)
admin.site.register(Aggregate)
