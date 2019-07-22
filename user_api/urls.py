from django.urls import path
from user_api.views import UserList, UserDetail, password_change, delete_account

urlpatterns = [
    path('api/users/', UserList.as_view()),
    path('api/user_settings/', UserDetail.as_view()),
    path('api/password_change/', password_change),
    path('api/delete_account/', delete_account),
]

