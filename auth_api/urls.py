from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView

from auth_api.views import AppTokenObtainPairView

urlpatterns = [
    # Rest JWT token auth
    path('api/auth/obtain_token/', AppTokenObtainPairView.as_view()),
    path('api/auth/refresh_token/', TokenRefreshView.as_view()),
    path('api/auth/verify_token/', TokenVerifyView.as_view()),
]