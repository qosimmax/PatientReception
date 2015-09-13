from django.contrib import admin
from .models import *


class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'doctor',
        'patient',
        'accept_time',
        'finish_time',
    )


# Register your models here.
admin.site.register([Doctor, Patient])
admin.site.register(Record, RecordAdmin)