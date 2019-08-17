from rest_framework import routers
from profile_image_api.views import ProfileImageSet

# Add in our routing for the profile image api

router = routers.DefaultRouter()
router.register(r'api/profile_image', ProfileImageSet, basename='person')

urlpatterns = router.urls
