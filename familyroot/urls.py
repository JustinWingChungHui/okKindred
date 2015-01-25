from django.conf.urls import patterns, include, url
from custom_user.views import login, auth_view
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:


    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', 'familyroot.views.about', name='about'),
    url(r'^$', 'familyroot.views.index', name='index'),

    #user auth urls
    url(r'^accounts/login/$', login),
    url(r'^accounts/auth/$', auth_view),
    url(r'^accounts/logout/$', 'custom_user.views.logout'),
    url(r'^accounts/logged_in/$', 'custom_user.views.logged_in'),
    url(r'^accounts/invalid/$', 'custom_user.views.invalid_login'),

    #Tree Views
    url(r'^home/$', 'family_tree.views.tree', name='tree'),
    url(r'^person=(?P<person_id>\d+)/$', 'family_tree.views.tree', name='tree'),

    #Profile Views
    url(r'^profile=(?P<person_id>\d+)/$', 'family_tree.views.profile', name='profile'),
    url(r'^profile=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.profile', name='profile'),

    #Maps Views
    url(r'^map/$', 'family_tree.views.map', name='map'),
    url(r'^map=(?P<person_id>\d+)/$', 'family_tree.views.map', name='map'),

    #Search Views
    url(r'^search/$', 'family_tree.views.search', name='search'),
    url(r'^get_search_results_json/$', 'family_tree.views.get_search_results_json', name='get_search_results'),

    #Edit Profile
    url(r'^edit_profile=(?P<person_id>\d+)/$', 'family_tree.views.edit_profile', name='edit_profile'),
    url(r'^edit_profile=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.edit_profile', name='edit_profile'),
    url(r'^update_person=(?P<person_id>\d+)/$', 'family_tree.views.update_person', name='update_person'),

    #Editing biography
    url(r'^edit_biography=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.edit_biography', name='edit_biography'),
    url(r'^update_biography=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.update_biography', name='update_biography'),

    url(r'^edit_profile_photo=(?P<person_id>\d+)/$', 'family_tree.views.edit_profile_photo', name='edit_profile_photo'),
    url(r'^image_upload=(?P<person_id>\d+)/$', 'family_tree.views.image_upload', name='image_upload'),
    url(r'^image_resize=(?P<person_id>\d+)/$', 'family_tree.views.image_resize', name='image_resize'),
    url(r'^image_crop=(?P<person_id>\d+)/$', 'family_tree.views.image_crop', name='image_crop'),


)
