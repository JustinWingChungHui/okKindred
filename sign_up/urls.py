from django.urls import path
import sign_up.views


urlpatterns = [
    path('accounts/sign_up/', sign_up.views.sign_up),
    path('accounts/sign_up_confirmation=<str:confirmation_key>/', sign_up.views.sign_up_confirmation),
]
