'''
Registers the models against an admin site
Only change is to foreign keys becoming raw ID fields to reduce load
'''
from gallery.models import Gallery, Image, Tag
from django.contrib import admin


class GalleryAdmin(admin.ModelAdmin):
    raw_id_fields = ('family',)

class ImageAdmin(admin.ModelAdmin):
    raw_id_fields = ('gallery',)

class TagAdmin(admin.ModelAdmin):
    raw_id_fields = ('image','person')


admin.site.register(Gallery,GalleryAdmin)
admin.site.register(Image,ImageAdmin)
admin.site.register(Tag,TagAdmin)