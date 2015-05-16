from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
#from django.conf.urls.i18n import i18n_patterns

admin.autodiscover()

#Translated urls
urlpatterns = patterns('',

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
    url(r'^accounts/auth/$', 'custom_user.views.auth_view'),
    url(r'^accounts/change_password/$', 'custom_user.views.change_password_post'),
    url(r'^accounts/update_settings/$', 'custom_user.views.update_user_setting_post'),
    url(r'^accounts/delete/$', 'custom_user.views.delete_account_post'),

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
    url(r'^add_relation_post=(?P<person_id>\d+)/$', 'family_tree.views.add_relation_post', name='add_relation_post'),
    url(r'^break_relation_post=(?P<person_id>\d+)/$', 'family_tree.views.break_relation_post', name='break_relation_post'),

    #Profile Views
    url(r'^profile=(?P<person_id>\d+)/$', 'family_tree.views.profile', name='profile'),
    url(r'^profile=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.profile', name='profile'),

    #Maps Views
    url(r'^map/$', 'family_tree.views.map', name='map'),
    url(r'^map=(?P<person_id>\d+)/$', 'family_tree.views.map', name='map'),
    url(r'^map_points/(?P<division_size>\d+\.\d+)/$', 'family_tree.views.map_points', name='map_points'),

    #Search Views
    url(r'^search/$', 'family_tree.views.search', name='search'),
    url(r'^get_search_results_json/$', 'family_tree.views.get_search_results_json', name='get_search_results'),

    #Edit Profile
    url(r'^edit_profile=(?P<person_id>\d+)/$', 'family_tree.views.edit_profile', name='edit_profile'),
    url(r'^edit_profile=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.edit_profile', name='edit_profile'),


    #Editing biography
    url(r'^edit_biography=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.edit_biography', name='edit_biography'),
    url(r'^update_biography=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.update_biography', name='update_biography'),

    #Profile Image views
    url(r'^edit_profile_photo=(?P<person_id>\d+)/$', 'family_tree.views.edit_profile_photo', name='edit_profile_photo'),
    url(r'^image_resize=(?P<person_id>\d+)/$', 'family_tree.views.image_resize', name='image_resize'),
    url(r'^update_person=(?P<person_id>\d+)/$', 'family_tree.views.update_person', name='update_person'),
    url(r'^image_crop=(?P<person_id>\d+)/$', 'family_tree.views.image_crop', name='image_crop'),
    url(r'^image_upload=(?P<person_id>\d+)/$', 'family_tree.views.image_upload', name='image_upload'),
    url(r'^delete=(?P<person_id>\d+)/$', 'family_tree.views.delete_profile', name='delete_profile'),

    #User Settings
    url(r'^settings/$', 'custom_user.views.settings_view', name='settings_view'),
    url(r'^accounts/invite_person=(?P<person_id>\d+)/$', 'email_confirmation.views.invite_person', name='invite_person'),

    #Gallery views
    url(r'^gallery/$', 'gallery.views.gallery_index', name='gallery_index'),
    url(r'^gallery/gallery_data=(?P<page>\d+)/$', 'gallery.views.gallery_index_data', name='gallery_index_data'),
    url(r'^new_gallery/$', 'gallery.views.edit_gallery', name='edit_gallery'),
    url(r'^gallery=(?P<gallery_id>\d+)/edit/$', 'gallery.views.edit_gallery', name='edit_gallery'),
    url(r'^gallery=(?P<gallery_id>\d+)/delete/$', 'gallery.views.delete_gallery', name='delete_gallery'),

    #Gallery Image views
    url(r'^gallery=(?P<gallery_id>\d+)/$', 'gallery.views.gallery', name='gallery'),
    url(r'^gallery=(?P<gallery_id>\d+)/image_data=(?P<page>\d+)/$', 'gallery.views.gallery_images', name='gallery_images'),
    url(r'^gallery=(?P<gallery_id>\d+)/upload_images/$', 'gallery.views.upload_images', name='upload_images'),
    url(r'^gallery=(?P<gallery_id>\d+)/upload_images_post/$', 'gallery.views.upload_images_post', name='upload_images_post'),

    #Image views
    url(r'^image=(?P<image_id>\d+)/details/$', 'gallery.views.image_detail', name='image_detail'),
    url(r'^image=(?P<image_id>\d+)/update/$', 'gallery.views.image_detail_update', name='image_detail_update'),
    url(r'^image=(?P<image_id>\d+)/delete/$', 'gallery.views.image_delete', name='image_delete'),
    url(r'^image=(?P<image_id>\d+)/make_gallery_thumbnail/$', 'gallery.views.set_image_as_gallery_thumbnail', name='set_image_as_gallery_thumbnail'),

    #Tagging API
    url(r'^image=(?P<image_id>\d+)/tags/get/$', 'gallery.views.get_tags', name='get_tags'),
    url(r'^tag=(?P<tag_id>\d+)/delete/$', 'gallery.views.delete_tag', name='delete_tag'),
    url(r'^image=(?P<image_id>\d+)/tags/create/$', 'gallery.views.create_tag', name='create_tag'),

    #Person Gallery Views
    url(r'^person=(?P<person_id>\d+)/photos/$', 'gallery.views.person_gallery', name='person_gallery'),
    url(r'^person=(?P<person_id>\d+)/photos/image=(?P<image_id>\d+)/$', 'gallery.views.person_gallery', name='person_gallery'),
    url(r'^person=(?P<person_id>\d+)/photos/image_data=(?P<page>\d+)/$', 'gallery.views.person_gallery_data', name='person_gallery_data'),

    #Gallery Map Views
    url(r'^gallery=(?P<gallery_id>\d+)/map/$', 'gallery.views.gallery_map', name='gallery_map'),
    url(r'^gallery=(?P<gallery_id>\d+)/map_data/(?P<division_size>\d+\.\d+)/$', 'gallery.views.gallery_map_data', name='gallery_map_data'),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^translate/', include('rosetta.urls')),
    )
