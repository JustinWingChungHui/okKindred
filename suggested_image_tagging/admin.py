'''
Registers the models against an admin site
Only change is to foreign keys becoming raw ID fields to reduce load
'''
from suggested_image_tagging.models import SuggestedTag
from django.contrib import admin


class SuggestedTagAdmin(admin.ModelAdmin):
    raw_id_fields = ('image','person')

admin.site.register(SuggestedTag,SuggestedTagAdmin)