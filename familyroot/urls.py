from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:


    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', 'familyroot.views.about', name='about'),
    url(r'^$', 'familyroot.views.index', name='index'),

    #user auth urls
    url(r'^accounts/login/$', 'custom_user.views.login'),
    url(r'^accounts/auth/$', 'custom_user.views.auth_view'),
    url(r'^accounts/logout/$', 'custom_user.views.logout'),
    url(r'^accounts/logged_in/$', 'custom_user.views.logged_in'),
    url(r'^accounts/invalid/$', 'custom_user.views.invalid_login'),

    #Tree Views

    url(r'^home/$', 'family_tree.views.tree', name='tree'),
    url(r'^person=(?P<person_id>\d+)/$', 'family_tree.views.tree', name='tree'),

    #Profile Views
    url(r'^profile=(?P<person_id>\d+)/$', 'family_tree.views.profile', name='profile'),
    url(r'^profile=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.profile', name='profile'),
    url(r'^edit_profile=(?P<person_id>\d+)/$', 'family_tree.views.edit_profile', name='edit_profile'),
    url(r'^edit_profile=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.edit_profile', name='edit_profile'),
    url(r'^update_person/$', 'family_tree.views.update_person', name='update_person'),
    url(r'^edit_biography=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.edit_biography', name='edit_biography'),
    url(r'^update_biography=(?P<person_id>\d+)/ln=(?P<requested_language>[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*)/$', 'family_tree.views.update_biography', name='update_biography'),
)
