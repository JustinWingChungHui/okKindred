from django.contrib import admin
from sign_up.models import SignUp

class SignUpAdmin(admin.ModelAdmin):
    pass

admin.site.register(SignUp,SignUpAdmin)
