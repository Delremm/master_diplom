# coding:utf-8
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views

from django import forms
from registration_email.forms import EmailAuthenticationForm
from registration_email.auth import EmailBackend

from django.views.generic import RedirectView
from django.views import generic

from django.http import HttpResponse

handler404 = 'django.views.defaults.page_not_found'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'master_diplom.views.home', name='home'),
    # url(r'^master_diplom/', include('master_diplom.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration_email.backends.simple.urls')),
    url(r'^', include('master_diplom_app.urls')),
    url(r'^/', RedirectView.as_view(url='/')),
    url(r'^robokassa/', include('robokassa.urls')),
    (r'^robots\.txt$', lambda r: HttpResponse("", mimetype="text/plain")),
    #(r'^grappelli/', include('grappelli.urls')),
    (r'^api/v2/', include('fiber.rest_api.urls')),
    (r'^admin/fiber/', include('fiber.admin_urls')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': ('fiber',),}),
    (r'', 'fiber.views.page'),
)
