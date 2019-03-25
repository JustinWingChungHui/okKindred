from rest_framework import routers
from person_api.views import PersonViewSet

# Add in our routing for the person api

router = routers.DefaultRouter()
router.register(r'api/person', PersonViewSet, basename='person')

urlpatterns = router.urls