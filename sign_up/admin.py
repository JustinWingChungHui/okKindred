from django.contrib import admin
from sign_up.models import SignUp

class SignUpAdmin(admin.ModelAdmin):
    list_display = ('email_address','ip_address','name','creation_date',)

admin.site.register(SignUp,SignUpAdmin)
