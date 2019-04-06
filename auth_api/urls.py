from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Rest JWT token auth
    path('api/auth/obtain_token/', TokenObtainPairView.as_view()),
    path('api/auth/refresh_token/', TokenRefreshView.as_view()),
    path('api/auth/verify_token/', TokenVerifyView.as_view()),
]