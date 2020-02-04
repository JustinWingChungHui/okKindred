from django.urls import path
from chinese_relation_name.views import family_member_names, relation_name

urlpatterns = [
    path('api/family_member_names/', family_member_names),
    path('api/relation_name/<int:from_person_id>/<int:to_person_id>/', relation_name),
]