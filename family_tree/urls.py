from django.urls import path
from django.views.generic.base import RedirectView

import family_tree.views


urlpatterns = [

    #Tree Views
    path('home/', RedirectView.as_view(url='/')), #Deprecated
    path('person=<int:person_id>/', family_tree.views.tree_app), #Deprecated
    path('how_am_i_related=<int:person_id>/', family_tree.views.how_am_i_related_view),
    path('descendants=<int:person_id>/', family_tree.views.get_descendants),
    path('ancestors=<int:person_id>/', family_tree.views.get_ancestors),

    path('tree/', family_tree.views.tree_app),
    path('tree/<int:person_id>/', family_tree.views.tree_app),
    path('tree/data/', family_tree.views.tree_data),

    #Not accessible yet
    path('tree/all/', family_tree.views.whole_tree),


    #Relation Views
    path('add_relation=<int:person_id>/', family_tree.views.add_relation_view),
    path('break_relation=<int:person_id>/', family_tree.views.break_relation_view),
    path('add_relation_post=<int:person_id>/', family_tree.views.add_relation_post),
    path('break_relation_post=<int:person_id>/', family_tree.views.break_relation_post),

    #Profile Views
    path('genders/', family_tree.views.genders, name='genders'),
    path('profile=<int:person_id>/', family_tree.views.profile),

    #Edit Profile
    path('edit_profile=<int:person_id>/', family_tree.views.edit_profile),
    path('update_person=<int:person_id>/', family_tree.views.update_person),

    #Search Views
    path('search/', family_tree.views.search),
    path('get_search_results_json/', family_tree.views.get_search_results_json),

    #Editing biography
    path('edit_biography=<int:person_id>/', family_tree.views.edit_biography),
    path('update_biography=<int:person_id>/', family_tree.views.update_biography),

    #Profile Image views
    path('edit_profile_photo=<int:person_id>/', family_tree.views.edit_profile_photo),
    path('image_resize=<int:person_id>/', family_tree.views.image_resize),
    path('image_crop=<int:person_id>/', family_tree.views.image_crop),
    path('image_rotate=<int:person_id>/', family_tree.views.image_rotate),
    path('image_upload=<int:person_id>/', family_tree.views.image_upload),
    path('delete=<int:person_id>/', family_tree.views.delete_profile),

]
