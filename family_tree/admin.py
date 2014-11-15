'''
Registers the models against an admin site
Only change is to foreign keys becoming raw ID fields to reduce load
'''

from family_tree.models import Person
from family_tree.models import Biography
from family_tree.models import Relation
from django.contrib import admin

class PersonAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)

admin.site.register(Person,PersonAdmin)


class BiographyAdmin(admin.ModelAdmin):
    raw_id_fields = ('person',)

admin.site.register(Biography,BiographyAdmin)

class RelationAdmin(admin.ModelAdmin):
    raw_id_fields = ('from_person','to_person')

admin.site.register(Relation,RelationAdmin)

