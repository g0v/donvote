from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from . import views

urlpatterns = patterns('vote.views',
    url(r'^api/vote/$', views.VoteList.as_view()),
    url(r'^api/vote/(?P<pk>[0-9]+)/$', views.VoteDetail.as_view()),
    url(r'^api/vote/(?P<discuss_owner_pk>[0-9]+)/discuss/$', views.VoteSubDiscussList.as_view()),
    url(r'^api/vote/(?P<karma_owner_pk>[0-9]+)/karma/$', views.VoteSubKarmaList.as_view()),
    url(r'^api/vote/(?P<plan_owner_pk>[0-9]+)/plan/$', views.VoteSubPlanList.as_view()),
    url(r'^api/vote/(?P<vote_pk>[0-9]+)/plan/(?P<plan_pk>[0-9]+)/ballot/$', views.BallotView.as_view()),
    url(r'^api/vote/(?P<vote_pk>[0-9]+)/plan/(?P<plan_pk>[0-9]+)/ballot/(?P<ballot_pk>[0-9]+)/$', views.BallotView.as_view()),
    url(r'^api/plan/$', views.PlanList.as_view()),
    url(r'^api/plan/(?P<pk>[0-9]+)/$', views.PlanDetail.as_view()),
    url(r'^api/discuss/$', views.DiscussList.as_view()),
    url(r'^api/discuss/(?P<pk>[0-9]+)/$', views.DiscussDetail.as_view()),
    #url(r'vote/$', TemplateView.as_view(template_name="votelist.jade")),
    url(r'^vote/$', views.VoteListPage.as_view()),
    url(r'^vote/new/$', views.VoteEditView.as_view()), #TemplateView.as_view(template_name="vote/new.jade")),
    url(r'^vote/(?P<pk>[0-9]+)/$', views.VoteDetailView.as_view()),
    url(r'^vote/(?P<pk>[0-9]+)/(?P<edit>edit)/$', views.VoteEditView.as_view()), #TemplateView.as_view(template_name="vote/new.jade")),
    #url(r'vote/(?P<pk>[0-9]+)/$', TemplateView.as_view(template_name="vote/detail.jade")),
)
