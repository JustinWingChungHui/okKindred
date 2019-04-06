from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from rest_framework.documentation import include_docs_urls


import okkindred.views

admin.autodiscover()

handler404 = 'okkindred.views.handler404'
handler505 = 'okkindred.views.handler405'

urlpatterns = [

    path('admin/', admin.site.urls),

    path('about/', okkindred.views.about, name='about'),
    path('languages/', okkindred.views.languages, name='languages'),
    path('', okkindred.views.index),

    #Custom user urls
    path('', include('custom_user.urls')),

    #Sign Up urls
    path('', include('sign_up.urls')),

    #Email confirmation views
    path('', include('email_confirmation.urls')),

    #Maps Views
    path('', include('maps.urls')),

    #Family Tree Views
    path('', include('family_tree.urls')),

    # Gallery views
    path('', include('gallery.urls')),

    # Django Rest Docs
    path('api/docs/', include_docs_urls(title='ok!Kindred APIs')),

    path('', include('auth_api.urls')),

    # Person API
    path('', include('person_api.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))



