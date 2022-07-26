from django.contrib import admin

from AI.models import BaseDevice, MediaFile

# Register your models here.
admin.site.register(BaseDevice)
admin.site.register(MediaFile)