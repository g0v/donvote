from django.shortcuts import render
from rest_framework import generics, permissions
from ..models import UserProfile
from ..serializers import UserProfileSerializer
from addon.permissions import IsOwnerOrReadOnly

class List(generics.ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileSerializer
  paginate_by = 5

  def get_queryset(self):
    username = self.request.QUERY_PARAMS.get("username",None)
    if username:
      return UserProfile.objects.filter(owner__username__icontains=username)
    else:
      return UserProfile.objects.all()

  def pre_save(self, obj):
    obj.owner = self.request.user

class Detail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileSerializer
