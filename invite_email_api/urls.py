from rest_framework import routers
from invite_email_api.views import InviteEmailViewSet, InviteEmailConfirmationViewSet

# Add in our routing for the person api

router = routers.DefaultRouter()
router.register(r'api/invite_email', InviteEmailViewSet, basename='invite_email')
router.register(r'api/invite_email_confirmation', InviteEmailConfirmationViewSet, basename='invite_email_confirmation')

urlpatterns = router.urls