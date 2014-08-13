from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Vote, Plan, Discuss, Karma, Ballot
import json

class PlanField(serializers.RelatedField):
  read_only = False
  def to_native(self, value):
    return {"id": value.pk, "name": value.name, "desc": value.desc}
  def from_native(self, data):
    p = Plan.objects.filter(pk=data.get("id") or -1)
    if len(p) > 0: return p[0]
    plan = PlanSerializer(data=data)
    if not plan.is_valid(): return None
    plan.object.owner = self.context["request"].user
    plan.object.save()
    return plan.object

class DiscussField(serializers.RelatedField):
  read_only = False
  def to_native(self, value):
    return {"id": value.pk, "content": value.content}
  def from_native(self, data):
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

class KarmaSerializer(serializers.ModelSerializer):
  owner = serializers.Field(source='owner.username')
  class Meta:
    model = Karma
    field = (  'value'  )

class DiscussSerializer(serializers.ModelSerializer):
  owner = serializers.Field(source='owner.username')
  class Meta:
    model = Discuss
    field = (  'owner', 'karma', 'createDate', 'modifyDate', 'content', 'tendency'  )

class BallotSerializer(serializers.ModelSerializer):
  owner = serializers.Field(source='owner.username')
  vote = serializers.PrimaryKeyRelatedField()
  plan = serializers.PrimaryKeyRelatedField()
  class Meta:
    model = Ballot
    field = ( 'owner', 'plan', 'vote', 'createDate', 'modifyDate' )

class VoteSerializer(serializers.ModelSerializer):
  owner = serializers.Field(source='owner.username')
  plan = PlanField(many=True)
  discuss = DiscussField(many=True)
  partial = True

  class Meta:
    model = Vote
    field = ( 
      # generic
      'owner', 'karma', 'discuss', 'name', 'desc', 'plan', 'ongoing', 
      'createDate', 'modifyDate',
      # start date
      'startMethod', 'startDate', 
        'needPlan', 'planCount', 
        'needKarma', 'karmaRate', 'karmaCount',
        'needQuality', 'qualifiedRate',
        'needAgree', 'agreeRate',
        'needAnwser', 'answerRate',
        'needStartCountDown', 'startCountDown',
      # end date
      'endMethod', 'endByDuration', 'endDate', 'duration',
        'needVote', 'voteRate',
        'needEndCountDown', 'endCountDown',
      # vote approach
      'voteMethod', 'maxChoiceCount', 'rankMethod'

      # cowork option
      'mute', 'noKarma', 'allowFork', 'allowNewPlan',

      # vote option
      'noProxy', 'disclosedBallot', 'allowAnonymous'
      
      # validation
      'allowNullTicket', 'useNullTicketRate', 'nullTicketRate',
      'useValidVoteRate', 'validVoteRate',
      'useObtainRate', 'obtainRate',
    )
    depth = 1
