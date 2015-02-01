'''
Registers the models against an admin site
Only change is to foreign keys becoming raw ID fields to reduce load
'''

from family_tree.models import Person, Biography, Relation, Family
from django.contrib import admin

class PersonAdmin(admin.ModelAdmin):

    fieldsets = [
          (None, {'fields': ['id','name','gender','family','locked','language','birth_year','year_of_death','photo'
          ,'small_thumbnail','large_thumbnail','email','telephone_number','website','address'
          ,'latitude','longitude','user','hierarchy_score']}),
          ('Tracking',  {'fields':['last_updated_date','creation_date'], 'classes': ['collapse']}),
          ]

    list_display = ('id','name','gender','last_updated_date','creation_date')
    search_fields = ['name']
    list_filter = ['creation_date','last_updated_date']
    readonly_fields = ('last_updated_date','creation_date','id')
    raw_id_fields = ('user','family')

admin.site.register(Person,PersonAdmin)


class BiographyAdmin(admin.ModelAdmin):
    raw_id_fields = ('person',)

admin.site.register(Biography,BiographyAdmin)

class RelationAdmin(admin.ModelAdmin):
    raw_id_fields = ('from_person','to_person')

admin.site.register(Relation,RelationAdmin)

admin.site.register(Family)

