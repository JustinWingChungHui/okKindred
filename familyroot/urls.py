from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
import familyroot.views
import custom_user.views
import email_confirmation.views
import family_tree.views
import gallery.views
import sign_up.views

admin.autodiscover()

#Translated urls
urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', familyroot.views.about, name='about'),
    url(r'^$', familyroot.views.index),

    #Custom user urls
    url(r'^accounts/login/$', custom_user.views.login),
    url(r'^accounts/logout/$', custom_user.views.logout),
    url(r'^accounts/logged_in/$', custom_user.views.logged_in),
    url(r'^accounts/invalid/$', custom_user.views.invalid_login),
    url(r'^accounts/auth/$', custom_user.views.auth_view),
    url(r'^accounts/change_password/$', custom_user.views.change_password_post),
    url(r'^accounts/update_settings/$', custom_user.views.update_user_setting_post),
    url(r'^accounts/delete/$', custom_user.views.delete_account_post),
    url(r'^settings/$', custom_user.views.settings_view),
    url(r'^accounts/password_reset/$', auth_views.password_reset, {'template_name': 'custom_user/password_reset.html'}, name='password_reset'),
    url(r'^accounts/password_reset/done/$', auth_views.password_reset_done, {'template_name': 'custom_user/password_reset_done.html'}, name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'template_name': 'custom_user/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', auth_views.password_reset_complete, {'template_name': 'custom_user/password_reset_complete.html'}, name='password_reset_complete'),

    #Sign Up urls
    url(r'^accounts/sign_up/$', sign_up.views.sign_up),
    url(r'^accounts/sign_up_confirmation=(?P<confirmation_key>\w+)/$', sign_up.views.sign_up_confirmation),

    #Email confirmation views
    url(r'^accounts/confirmation=(?P<confirmation_key>\w+)/$', email_confirmation.views.confirm_invite),
    url(r'^accounts/invalid_expired/$', email_confirmation.views.invalid_expired),
    url(r'^accounts/invite_person=(?P<person_id>\d+)/$', email_confirmation.views.invite_person),

    #Tree Views
    url(r'^home/$', family_tree.views.tree),
    url(r'^person=(?P<person_id>\d+)/$', family_tree.views.tree),
    url(r'^how_am_i_related=(?P<person_id>\d+)/$', family_tree.views.how_am_i_related_view),
    url(r'^descendants=(?P<person_id>\d+)/$', family_tree.views.get_descendants),
    url(r'^ancestors=(?P<person_id>\d+)/$', family_tree.views.get_ancestors),

    url(r'tree/$', family_tree.views.tree_app),
    url(r'tree/(?P<person_id>\d+)/$', family_tree.views.tree_app),
    url(r'^tree/data/$', family_tree.views.tree_data),

    #Not accessible yet
    url(r'^whole_tree/$', family_tree.views.whole_tree),


    #Relation Views
    url(r'^add_relation=(?P<person_id>\d+)/$', family_tree.views.add_relation_view),
    url(r'^break_relation=(?P<person_id>\d+)/$', family_tree.views.break_relation_view),
    url(r'^add_relation_post=(?P<person_id>\d+)/$', family_tree.views.add_relation_post),
    url(r'^break_relation_post=(?P<person_id>\d+)/$', family_tree.views.break_relation_post),

    #Profile Views
    url(r'^profile=(?P<person_id>\d+)/$', family_tree.views.profile),
    url(r'^profile=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', family_tree.views.profile),

    #Maps Views
    url(r'^map/$', family_tree.views.map),
    url(r'^map=(?P<person_id>\d+)/$', family_tree.views.map),
    url(r'^map_points/(?P<division_size>\d+\.\d+)/$', family_tree.views.map_points),

    #Search Views
    url(r'^search/$', family_tree.views.search),
    url(r'^get_search_results_json/$', family_tree.views.get_search_results_json),

    #Edit Profile
    url(r'^edit_profile=(?P<person_id>\d+)/$', family_tree.views.edit_profile),
    url(r'^edit_profile=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', family_tree.views.edit_profile),
    url(r'^update_person=(?P<person_id>\d+)/$', family_tree.views.update_person),

    #Editing biography
    url(r'^edit_biography=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', family_tree.views.edit_biography),
    url(r'^update_biography=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', family_tree.views.update_biography),

    #Profile Image views
    url(r'^edit_profile_photo=(?P<person_id>\d+)/$', family_tree.views.edit_profile_photo),
    url(r'^image_resize=(?P<person_id>\d+)/$', family_tree.views.image_resize),
    url(r'^image_crop=(?P<person_id>\d+)/$', family_tree.views.image_crop),
    url(r'^image_upload=(?P<person_id>\d+)/$', family_tree.views.image_upload),
    url(r'^delete=(?P<person_id>\d+)/$', family_tree.views.delete_profile),

    #Gallery views
    url(r'^gallery/$', gallery.views.gallery_index),
    url(r'^gallery/gallery_data=(?P<page>\d+)/$', gallery.views.gallery_index_data),
    url(r'^new_gallery/$', gallery.views.edit_gallery),
    url(r'^gallery=(?P<gallery_id>\d+)/edit/$', gallery.views.edit_gallery),
    url(r'^gallery=(?P<gallery_id>\d+)/delete/$', gallery.views.delete_gallery),

    #Gallery Image views
    url(r'^gallery=(?P<gallery_id>\d+)/$', gallery.views.gallery),
    url(r'^gallery=(?P<gallery_id>\d+)/image_data=(?P<page>\d+)/$', gallery.views.gallery_images),
    url(r'^gallery=(?P<gallery_id>\d+)/upload_images/$', gallery.views.upload_images),
    url(r'^gallery=(?P<gallery_id>\d+)/upload_images_post/$', gallery.views.upload_images_post),

    #Image views
    url(r'^image=(?P<image_id>\d+)/details/$', gallery.views.image_detail),
    url(r'^image=(?P<image_id>\d+)/update/$', gallery.views.image_detail_update),
    url(r'^image=(?P<image_id>\d+)/delete/$', gallery.views.image_delete),
    url(r'^image=(?P<image_id>\d+)/make_gallery_thumbnail/$', gallery.views.set_image_as_gallery_thumbnail),

    #Tagging API
    url(r'^image=(?P<image_id>\d+)/tags/get/$', gallery.views.get_tags),
    url(r'^tag=(?P<tag_id>\d+)/delete/$', gallery.views.delete_tag),
    url(r'^image=(?P<image_id>\d+)/tags/create/$', gallery.views.create_tag),

    #Person Gallery Views
    url(r'^person=(?P<person_id>\d+)/photos/$', gallery.views.person_gallery),
    url(r'^person=(?P<person_id>\d+)/photos/image=(?P<image_id>\d+)/$', gallery.views.person_gallery),
    url(r'^person=(?P<person_id>\d+)/photos/image_data=(?P<page>\d+)/$', gallery.views.person_gallery_data),

    #Gallery Map Views
    url(r'^gallery=(?P<gallery_id>\d+)/map/$', gallery.views.gallery_map),
    url(r'^gallery=(?P<gallery_id>\d+)/map_data/(?P<division_size>\d+\.\d+)/$', gallery.views.gallery_map_data),
    url(r'^image=(?P<image_id>\d+)/address/$', gallery.views.geocode_image_location_post),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^translate/', include('rosetta.urls')))


