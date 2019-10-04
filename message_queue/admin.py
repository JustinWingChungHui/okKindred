'''
Registers the models against an admin site
Only change is to foreign keys becoming raw ID fields to reduce load
'''
from message_queue.models import Queue, Message
from django.contrib import admin


class QueueAdmin(admin.ModelAdmin):
    list_display = ('id','name','description')

    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    # Remove delete actions
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(QueueAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','queue','processed','last_updated_date','creation_date')
    list_filter = (
        ('processed', admin.BooleanFieldListFilter),
    )

    ordering = ('-creation_date',)


admin.site.register(Queue,QueueAdmin)
admin.site.register(Message,MessageAdmin)
