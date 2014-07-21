from django.shortcuts import render
from rest_framework import generics, permissions
from .models import UserProfile, WorkGroup
from .serializers import UserProfileSerializer, WorkGroupSerializer
from .permissions import IsOwnerOrReadOnly

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
