from rest_framework import routers
from relation_api.views import RelationViewSet

# Add in our routing for the relation api

router = routers.DefaultRouter()
router.register(r'api/relation', RelationViewSet, basename='relation')

urlpatterns = router.urls