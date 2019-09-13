from rest_framework import routers
from image_tagging_api.views import TagView

# Add in our routing for the image tagging api

router = routers.DefaultRouter()
router.register(prefix=r'api/image_tagging', viewset=TagView, basename='tag')

urlpatterns = router.urls
