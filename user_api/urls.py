from django.urls import path
from user_api.views import UserDetail

urlpatterns = [
    path('api/account/', UserDetail.as_view()),
]

