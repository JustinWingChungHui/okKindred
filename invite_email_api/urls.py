from rest_framework import routers
from invite_email_api.views import InviteEmailViewSet

# Add in our routing for the person api

router = routers.DefaultRouter()
router.register(r'api/invite_email', InviteEmailViewSet, basename='invite_email')

urlpatterns = router.urls