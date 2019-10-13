from facial_recognition.models import FaceModel
from django.contrib import admin


class FaceModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(FaceModel, FaceModelAdmin)

