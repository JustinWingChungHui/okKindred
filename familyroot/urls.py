from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    url(r'^$', 'familyroot.views.index', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', 'familyroot.views.about', name='about'),

    #user auth urls
    url(r'^accounts/login/$', 'familyroot.views.login'),
    url(r'^accounts/auth/$', 'familyroot.views.auth_view'),
    url(r'^accounts/logout/$', 'familyroot.views.logout'),
    url(r'^accounts/logged_in/$', 'familyroot.views.logged_in'),
    url(r'^accounts/invalid/$', 'familyroot.views.invalid_login'),

)