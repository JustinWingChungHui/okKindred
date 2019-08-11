from rest_framework import routers
from sign_up_api.views import SignUpViewSet

# Add in our routing for the person api

router = routers.DefaultRouter()
router.register(r'api/sign_up', SignUpViewSet, basename='sign_up')

urlpatterns = router.urls