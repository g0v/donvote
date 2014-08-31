from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from . import views

urlpatterns = patterns('account.views',
    # API
    url(r'^api/user/$', views.user.ListAPI.as_view(),name="api_user_list"),
    url(r'^api/user/(?P<pk>[0-9]+)/$', views.user.DetailAPI.as_view()),
    url(r'^api/group/$', views.group.ListAPI.as_view(),name="api_group_list"),
    url(r'^api/group/new/$', views.group.ListAPI.as_view(),name="api_create_group"),
    url(r'^api/group/(?P<pk>[0-9]+)/$', views.group.DetailAPI.as_view()),
    url(r'^api/group/(?P<vote_owner_id>[0-9]+)/vote/$', views.group.VoteList.as_view(), name="api_group_add_vote"),  
    url(r'^api/group/(?P<discuss_owner_pk>[0-9]+)/discuss/$', views.group.DiscussList.as_view(),name="group_discuss_api"),

    # View
    url(r'^group/new/$', views.group.EditView.as_view()),
    url(r'^group/(?P<id>[0-9]+)/vote/new/$', views.group.NewVote.as_view(),name="new_vote_of_group"),
    url(r'^group/(?P<id>[0-9]+)/$', views.group.DetailView.as_view()),
)

