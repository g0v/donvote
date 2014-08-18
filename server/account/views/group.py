from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.core.urlresolvers import reverse
from rest_framework import generics, permissions
from ..models import WorkGroup
from ..serializers import WorkGroupSerializer
from addon.permissions import IsOwnerOrReadOnly
from addon.views import SubView
from vote.views import DiscussList, VoteList
from vote import views as VoteViews

class List(generics.ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
  queryset = WorkGroup.objects.all()
  serializer_class = WorkGroupSerializer
  filter_fields = ('name')
  def pre_save(self, obj):
    obj.owner = self.request.user

class Detail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
  queryset = WorkGroup.objects.all()
  serializer_class = WorkGroupSerializer

class Edit(TemplateView):
  template_name = "group/edit.jade"

class WorkGroupDetailView(TemplateView):
  template_name = "group/detail.jade"
  def get_context_data(self, **kwargs):
    context = super(WorkGroupDetailView, self).get_context_data(**kwargs)
    group = WorkGroup.objects.filter(pk=kwargs['pk'])
    context["ownerapi"] = reverse("group_discuss_api", kwargs={"discuss_owner_pk": kwargs["pk"]})
    context['group'] = group[0] if len(group) else None
    return context

@SubView
class DiscussList(VoteViews.DiscussList):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
  root_class = WorkGroup
  target_field = "discuss"

@SubView
class VoteList(VoteViews.VoteList):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
  root_class = WorkGroup
  target_field = "vote"

class NewVote(TemplateView):
  template_name = "vote/edit.jade"
  def get_context_data(self, **kwargs):
    context = super(WorkGroupNewVoteView, self).get_context_data(**kwargs)
    context["ownerapi"] = reverse("group_vote_api", kwargs={"vote_owner_pk": kwargs["vote_owner_pk"]})
    return context
