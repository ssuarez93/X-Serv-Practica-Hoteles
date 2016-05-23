from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.models import User

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', 'Hoteles.views.login_correcto'),
    url(r'^logout$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/profile/$', 'Hoteles.views.login_correcto'),
    url(r'^about$', 'Hoteles.views.about'),
    url(r'^(style\D\d+.css)$', 'django.views.static.serve', {
                        'document_root': 'templates/WesternNightLights/'}),
    url(r'^(style.css)$', 'django.views.static.serve', {
                        'document_root': 'templates/WesternNightLights/'}),
    url(r'^img/(.*)$', 'django.views.static.serve', {
                        'document_root': 'templates/WesternNightLights/img/'}),
    url(r'^alojamientos/(style.css)$', 'django.views.static.serve', {
                        'document_root': 'templates/WesternNightLights/'}),
    url(r'^alojamientos/(style\D\d+.css)$', 'django.views.static.serve', {
                        'document_root': 'templates/WesternNightLights/'}),
    url(r'^alojamientos/img/(.*)$', 'django.views.static.serve', {
                        'document_root': 'templates/WesternNightLights/img/'}),
    url(r'^alojamientos$', 'Hoteles.views.alojamientos'),
    url(r'^alojamientos/(\d+)$', 'Hoteles.views.aloj_id'),
    url(r'^$', 'Hoteles.views.principal'),
    url(r'^index.html$', 'Hoteles.views.principal'),
    url(r'/?(.*)/xml', 'Hoteles.views.profile_xml'),
    url(r'^(.*)$', 'Hoteles.views.profile')

)
