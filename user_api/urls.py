from django.urls import path
from user_api.views import UserDetail, password_change

urlpatterns = [
    path('api/usersettings/', UserDetail.as_view()),
    path('api/password_change/', password_change),
]

