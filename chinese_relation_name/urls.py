from django.urls import path
from chinese_relation_name.views import family_member_names

urlpatterns = [
    path('api/family_member_names/', family_member_names),
]