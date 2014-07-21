from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Vote, Plan, Discuss
import json

class BlahField(serializers.RelatedField):
  read_only = False
  def to_native(self, value):
    return {"id": value.pk, "name": value.name}
  def from_native(self, data):
    p = Plan.objects.filter(pk=data.get("id") or -1)
    if len(p) > 0: return p[0]
    plan = PlanSerializer(data=data)
    if not plan.is_valid(): return None
    plan.object.owner = self.context["request"].user
    plan.object.save()
    return plan.object

class Blah2Field(serializers.RelatedField):
  read_only = False
  def to_native(self, value):
    return {"id": value.pk, "content": value.content}
  def from_native(self, data):
    print("blah2: i am going to create a field")
    d = Discuss.objects.filter(pk=data.get("id") or -1)
    if len(d) > 0: return d[0]
    discuss = DiscussSerializer(data=data)
    if not discuss.is_valid(): return None
    discuss.object.owner = self.context["request"].user
    discuss.object.save()
    return discuss.object

class PlanSerializer(serializers.ModelSerializer):
  owner = serializers.Field(source='owner.username')
  class Meta:
    model = Plan
    field = (  'owner', 'karma', 'discuss', 'createDate', 'modifyDate', 'name', 'desc')

class DiscussSerializer(serializers.ModelSerializer):
  owner = serializers.Field(source='owner.username')
  class Meta:
    model = Discuss
    field = (  'owner', 'karma', 'createDate', 'modifyDate', 'content')

class VoteSerializer(serializers.ModelSerializer):
  owner = serializers.Field(source='owner.username')
  plan = BlahField(many=True)
  discuss = Blah2Field(many=True)
  partial = True

  class Meta:
    model = Vote
    field = ( 'owner', 'karma', 'discuss', 'plan', 'ongoing', 'startMethod',
      'startDate', 'needKarma', 'needPlan', 'needQuality', 'needAgree',
      'karmaRate', 'planCount', 'planKarmaRate', 'planQualifiedRate',
      'closeQustionRate', 'autoStartCountdown', 'AgreeRate', 'endMethod',
      'duration', 'voteRate', 'autoEndCountdown', 'voteMethod',
      'maxChoiceCount', 'disclosedBallot', 'allowAnonymous', 'allowNullTicket',
      'validCriteria', 'newPlanFromAll', 'invalidNullTickRate', 'validVoteRate',
      'createDate', 'modifyDate', 'planlist'
    )
    depth = 1
