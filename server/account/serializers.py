from rest_framework import serializers
from .models import UserProfile, WorkGroup, NameList
from vote.serializers import DiscussField, PlanField, KarmaField, VoteField
from django.contrib.auth.models import User
from addon.serializers import DetailRelatedField, WritableDetailRelatedField

class SimpleUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username')

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'last_name', 'first_name', 'username')

class UserField(DetailRelatedField):
  serializer = UserSerializer

class SimpleUserField(DetailRelatedField):
  read_only = False
  serializer = SimpleUserSerializer

class UserProfileSerializer(serializers.ModelSerializer):
  group = serializers.PrimaryKeyRelatedField(many=True)
  owner = UserField()
  class Meta:
    model = UserProfile
    fields = ('id', 'group', 'owner')

class DeptField(WritableDetailRelatedField):
  def to_native(self, value):
    return {"id": value.id, "name": value.name}

class WorkGroupSerializer(serializers.ModelSerializer):
  owner = UserField()
  karma = KarmaField()
  dept = DeptField(many=True)
  vote = VoteField(many=True)
  staff = SimpleUserField(many=True)
  member = SimpleUserField(many=True)
  partial = True
  class Meta:
    model = WorkGroup
    fields = ('id','name','desc','karma','dept','vote','staff','member','owner')
  depth = 1

