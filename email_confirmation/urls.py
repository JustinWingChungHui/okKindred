from django.urls import path
import email_confirmation.views


urlpatterns = [
    path('accounts/confirmation=<str:confirmation_key>/', email_confirmation.views.confirm_invite),
    path('accounts/invalid_expired/', email_confirmation.views.invalid_expired),
    path('accounts/invite_person=<int:person_id>/', email_confirmation.views.invite_person),
]
