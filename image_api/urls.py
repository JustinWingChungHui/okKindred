from rest_framework import routers
from image_api.views import ImageListView

# Add in our routing for the image api

router = routers.DefaultRouter()
router.register(r'api/image', ImageListView, basename='image')

urlpatterns = router.urls