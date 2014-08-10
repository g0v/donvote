from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'donvote.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('account.urls')),

    url(r'^$', TemplateView.as_view(template_name = "landing.jade")),
    url(r'^dev/?$', TemplateView.as_view(template_name = "dev.jade")),
    url(r'^new/?$', TemplateView.as_view(template_name = "new.jade")),
    url(r'^', include('vote.urls')),
)
