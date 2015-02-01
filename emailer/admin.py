from django.contrib import admin
from emailer.models import Email, FamilyNewsLetterEvents

class EmailAdmin(admin.ModelAdmin):
    '''
    Represents the admin user interface for the email object
    '''
    fieldsets = [
              (None, {'fields': ['id','recipient','subject','content','content_html','send_attempts','send_successful']}),
              ]

    list_display = ('id','recipient','send_attempts','send_successful')
    search_fields = ['recipient']
    list_filter = ['send_successful','send_attempts']
    readonly_fields = ('id','send_successful')

admin.site.register(Email,EmailAdmin)


class FamilyNewsLetterEventsAdmin(admin.ModelAdmin):
    '''
    Represents the admin user interface for the email object
    '''
    fieldsets = [
              (None, {'fields': ['id','family_id','person_id','person_name','new_member','creation_date',]}),
              ]

    list_display = ('id','person_name','new_member','creation_date')
    search_fields = ['person_name']
    readonly_fields = ('id','creation_date')


admin.site.register(FamilyNewsLetterEvents, FamilyNewsLetterEventsAdmin)