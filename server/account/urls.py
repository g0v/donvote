from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('account.views',
    url(r'^api/user/$', views.UserProfileList.as_view()),
    url(r'^api/user/(?P<pk>[0-9]+)/$', views.UserProfileDetail.as_view()),
    url(r'^api/group/$', views.WorkGroupList.as_view()),
    url(r'^api/group/(?P<pk>[0-9]+)/$', views.WorkGroupDetail.as_view()),
    url(r'^api/group/(?P<discuss_owner_pk>[0-9]+)/discuss/$', views.WorkGroupSubDiscussList.as_view(),name="group_discuss_api"),

    url(r'group/new/$', views.WorkGroupEditView.as_view()),
    url(r'group/(?P<pk>[0-9]+)/$', views.WorkGroupDetailView.as_view()),
    url(r'group/(?P<vote_owner_pk>[0-9]+)/vote/new/$', views.WorkGroupSubVoteList.as_view()),  
)

