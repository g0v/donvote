from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('account.views',
    url(r'^user/$', views.UserProfileList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserProfileDetail.as_view()),
    url(r'^group/$', views.WorkGroupList.as_view()),
    url(r'^group/(?P<pk>[0-9]+)/$', views.WorkGroupDetail.as_view()),
)

