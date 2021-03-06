from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from people.views import UserProfileView

urlpatterns = patterns('',

    url(r'^', include('ui.urls')),
    url(r'^cfp/', include('cfp.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', UserProfileView.as_view(), name='user_profile'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
    )

