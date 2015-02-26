from django.contrib import admin
from email_confirmation.models import EmailConfirmation

# Register your models here.
class EmailConfirmationAdmin(admin.ModelAdmin):
    raw_id_fields = ('person','user_who_invited_person')

admin.site.register(EmailConfirmation,EmailConfirmationAdmin)