from rest_framework import generics
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly, VotePermission, PlanPermission
from .serializers import VoteSerializer, PlanSerializer, DiscussSerializer
from .models import Vote, Plan, Discuss

class VoteList(generics.ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
  queryset = Vote.objects.all()
  serializer_class = VoteSerializer
  def pre_save(self, obj):
    if not obj.owner_id: obj.owner = self.request.user

class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,VotePermission)
  queryset = Vote.objects.all()
  serializer_class = VoteSerializer
  def pre_save(self, obj):
    if not obj.owner_id: obj.owner = self.request.user

class PlanList(generics.ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,PlanPermission)
  queryset = Plan.objects.all()
  serializer_class = PlanSerializer
  def pre_save(self, obj):
    obj.owner = self.request.user

class PlanDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
  queryset = Plan.objects.all()
  serializer_class = PlanSerializer
  def pre_save(self, obj):
    obj.owner = self.request.user


class DiscussList(generics.ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
  queryset = Discuss.objects.all()
  serializer_class = DiscussSerializer
  def pre_save(self, obj):
    obj.owner = self.request.user

class DiscussDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
  queryset = Discuss.objects.all()
  serializer_class = DiscussSerializer
  def pre_save(self, obj):
    obj.owner = self.request.user
