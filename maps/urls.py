from django.urls import path
import maps.views


urlpatterns = [
    path('map/', maps.views.map),
    path('map=<int:person_id>/', maps.views.map),
    path('map_points/', maps.views.map_points),
]
