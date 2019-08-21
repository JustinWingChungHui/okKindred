from rest_framework import routers
from gallery_api.views import GalleryView

# Add in our routing for the gallery api

router = routers.DefaultRouter()
router.register(r'api/gallery', GalleryView, basename='gallery')

urlpatterns = router.urls