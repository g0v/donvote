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
from django.http import Http404

class ListAPI(generics.ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
  queryset = WorkGroup.objects.all()
  serializer_class = WorkGroupSerializer
  filter_fields = ('name')
  paginate_by = 5
  def get_queryset(self):
    name = self.request.QUERY_PARAMS.get("name",None)
    if name:
      return WorkGroup.objects.filter(name__icontains=name)
    else:
      return WorkGroup.objects.all()

  def pre_save(self, obj):
    obj.owner = self.request.user

class DetailAPI(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
  queryset = WorkGroup.objects.all()
  serializer_class = WorkGroupSerializer

class EditView(TemplateView):
  template_name = "group/edit.jade"

class DetailView(TemplateView):
  template_name = "group/detail.jade"
  def get_context_data(self, **kwargs):
    context = super(DetailView, self).get_context_data(**kwargs)
    try: group = WorkGroup.objects.get(id=kwargs["id"])
    except: raise Http404()
    context["resInit"] = [{"name": "group", "obj": group, "serializer": WorkGroupSerializer}]
    return context

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

