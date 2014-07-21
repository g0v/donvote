from rest_framework import serializers
from .models import UserProfile, WorkGroup


class UserProfileSerializer(serializers.ModelSerializer):
  group = serializers.PrimaryKeyRelatedField(many=True)
  username = serializers.Field(source='owner.username')
  class Meta:
    model = UserProfile
    fields = ('id', 'group', 'username')


class WorkGroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = WorkGroup
    fields = ('id','name','desc')

