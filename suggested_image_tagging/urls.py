from rest_framework import routers
from suggested_image_tagging.views import SuggestedTagView

# Add in our routing for the image tagging api

router = routers.DefaultRouter()
router.register(prefix=r'api/suggested_image_tagging', viewset=SuggestedTagView, basename='tag')

urlpatterns = router.urls
