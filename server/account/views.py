from django.shortcuts import render
from django.views.generic import TemplateView, View
from rest_framework import generics, permissions
from .models import UserProfile, WorkGroup
from .serializers import UserProfileSerializer, WorkGroupSerializer
from addon.permissions import IsOwnerOrReadOnly
from addon.views import SubView
from vote.views import DiscussList, VoteList

# Create your views here.

class UserProfileList(generics.ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileSerializer
  def pre_save(self, obj):
    obj.owner = self.request.user

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileSerializer

class WorkGroupList(generics.ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
  queryset = WorkGroup.objects.all()
  serializer_class = WorkGroupSerializer
  def pre_save(self, obj):
    obj.owner = self.request.user

class WorkGroupDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
  queryset = WorkGroup.objects.all()
  serializer_class = WorkGroupSerializer

class WorkGroupEditView(TemplateView):
  template_name = "group/edit.jade"

class WorkGroupDetailView(TemplateView):
  template_name = "group/detail.jade"
  def get_context_data(self, **kwargs):
    context = super(WorkGroupDetailView, self).get_context_data(**kwargs)
    group = WorkGroup.objects.filter(pk=kwargs['pk'])
    context['group'] = group[0] if len(group) else None
    return context

@SubView
class WorkGroupSubDiscussList(DiscussList):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
  root_class = WorkGroup
  target_field = "discuss"

@SubView
class WorkGroupSubVoteList(VoteList):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
  root_class = WorkGroup
  target_field = "vote"

