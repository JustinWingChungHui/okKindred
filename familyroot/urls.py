from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
#from django.conf.urls.i18n import i18n_patterns

admin.autodiscover()

#Non-tranlated urls.  These will be mostly post views etc
urlpatterns = patterns('',
    url(r'^accounts/auth/$', 'custom_user.views.auth_view'),
    url(r'^accounts/change_password/$', 'custom_user.views.change_password_post'),
    url(r'^accounts/update_settings/$', 'custom_user.views.update_user_setting_post'),
    url(r'^accounts/delete/$', 'custom_user.views.delete_account_post'),
    url(r'^update_person=(?P<person_id>\d+)/$', 'family_tree.views.update_person', name='update_person'),
    url(r'^update_biography=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.update_biography', name='update_biography'),
    url(r'^image_crop=(?P<person_id>\d+)/$', 'family_tree.views.image_crop', name='image_crop'),
    url(r'^image_upload=(?P<person_id>\d+)/$', 'family_tree.views.image_upload', name='image_upload'),
    url(r'^get_search_results_json/$', 'family_tree.views.get_search_results_json', name='get_search_results'),
    url(r'^delete=(?P<person_id>\d+)/$', 'family_tree.views.delete_profile', name='delete_profile'),
    url(r'^add_relation_post=(?P<person_id>\d+)/$', 'family_tree.views.add_relation_post', name='add_relation_post'),
    url(r'^break_relation_post=(?P<person_id>\d+)/$', 'family_tree.views.break_relation_post', name='break_relation_post'),
    url(r'^accounts/invite_person=(?P<person_id>\d+)/$', 'email_confirmation.views.invite_person', name='invite_person'),
)



#Translated urls
urlpatterns += patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', 'familyroot.views.about', name='about'),
    url(r'^$', 'familyroot.views.index', name='index'),

    #user auth urls
    url(r'^accounts/login/$', 'custom_user.views.login'),
    url(r'^accounts/logout/$', 'custom_user.views.logout'),
    url(r'^accounts/logged_in/$', 'custom_user.views.logged_in'),
    url(r'^accounts/invalid/$', 'custom_user.views.invalid_login'),
    url(r'^accounts/confirmation=(?P<confirmation_key>\w+)/$', 'email_confirmation.views.confirm_invite'),
    url(r'^accounts/invalid_expired/$', 'email_confirmation.views.invalid_expired'),

    #Tree Views
    url(r'^home/$', 'family_tree.views.tree', name='tree'),
    url(r'^person=(?P<person_id>\d+)/$', 'family_tree.views.tree', name='tree'),
    url(r'^how_am_i_related=(?P<person_id>\d+)/$', 'family_tree.views.how_am_i_related_view', name='tree'),
    url(r'^descendants=(?P<person_id>\d+)/$', 'family_tree.views.get_descendants', name='get_descendants'),
    url(r'^ancestors=(?P<person_id>\d+)/$', 'family_tree.views.get_ancestors', name='get_ancestors'),

    #Not accessible yet
    url(r'^whole_tree/$', 'family_tree.views.whole_tree', name='whole_tree'),


    #Relation Views
    url(r'^add_relation=(?P<person_id>\d+)/$', 'family_tree.views.add_relation_view', name='add_relation_view'),
    url(r'^break_relation=(?P<person_id>\d+)/$', 'family_tree.views.break_relation_view', name='break_relation_view'),

    #Profile Views
    url(r'^profile=(?P<person_id>\d+)/$', 'family_tree.views.profile', name='profile'),
    url(r'^profile=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.profile', name='profile'),

    #Maps Views
    url(r'^map/$', 'family_tree.views.open_map', name='open_map'),
    url(r'^map=(?P<person_id>\d+)/$', 'family_tree.views.open_map', name='open_map'),

    #Search Views
    url(r'^search/$', 'family_tree.views.search', name='search'),


    #Edit Profile
    url(r'^edit_profile=(?P<person_id>\d+)/$', 'family_tree.views.edit_profile', name='edit_profile'),
    url(r'^edit_profile=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.edit_profile', name='edit_profile'),


    #Editing biography
    url(r'^edit_biography=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.edit_biography', name='edit_biography'),


    #Image views
    url(r'^edit_profile_photo=(?P<person_id>\d+)/$', 'family_tree.views.edit_profile_photo', name='edit_profile_photo'),
    url(r'^image_resize=(?P<person_id>\d+)/$', 'family_tree.views.image_resize', name='image_resize'),


    #User Settings
    url(r'^settings/$', 'custom_user.views.settings_view', name='settings_view'),

    #Gallery views
    url(r'^gallery/$', 'gallery.views.gallery_index', name='gallery_index'),
    url(r'^gallery/gallery_data=(?P<page>\d+)/$', 'gallery.views.gallery_data', name='gallery_data'),

)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^translate/', include('rosetta.urls')),
    )
