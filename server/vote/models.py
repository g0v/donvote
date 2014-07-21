# -*- coding: utf-8 -*-
from django.db import models
from donvote import utils
from django.contrib.auth.models import User, Group

# Create your models here.

class WithDateModel(models.Model):
  createDate = models.DateTimeField(auto_now_add=True)
  modifyDate = models.DateTimeField(auto_now=True)

class WithDescModel(WithDateModel):
  name = models.CharField(max_length=100,blank=False)
  desc = models.TextField(blank=True)
  thumb = models.ImageField(blank=True,upload_to="/tmp/")

class Karma(models.Model):
  owner = models.ForeignKey('auth.User', related_name="karma")
  VALUE = (
      ('0','neutral'),
      ('1','positive'),
      ('2','negative'),
  )
  value = models.CharField(max_length=1, choices=VALUE, default='0')

class Discuss(WithDateModel):
  owner = models.ForeignKey('auth.User', related_name="discuss")
  karma = models.ManyToManyField(Karma,blank=True)
  content = models.TextField(blank=False)

class Plan(WithDescModel):
  owner = models.ForeignKey('auth.User', related_name="plan")
  karma = models.ManyToManyField(Karma,blank=True)
  discuss = models.ManyToManyField(Discuss,blank=True)

class Vote(WithDateModel):
  owner = models.ForeignKey('auth.User', related_name="vote")
  karma = models.ManyToManyField(Karma,blank=True)
  discuss = models.ManyToManyField(Discuss,blank=True)

  name = models.CharField(max_length=100,blank=False)
  desc = models.TextField(blank=True)

  START_END_METHODS = (
      ('1', 'time'),
      ('2', 'criteria'),
      ('3', 'manually'),
  )

  VOTE_METHODS = (
      ('1', 'single'),
      ('2', 'multiple'),
      ('3', 'ranking'),
  )

  plan = models.ManyToManyField(Plan,blank=True)
  ongoing = models.BooleanField(default=False)

  # start method and criteria
  startMethod = models.CharField(max_length=1,choices=START_END_METHODS, default='1')
  startDate = models.DateTimeField(blank=True,null=True)
  needKarma = models.BooleanField(default=False)
  needPlan = models.BooleanField(default=False)
  needQuality = models.BooleanField(default=False)
  needAgree = models.BooleanField(default=False)
  needCloseQuestion = models.BooleanField(default=False)
  karmaRate = models.FloatField(default=0.25)
  planCount = models.IntegerField(default=3)
  planKarmaRate = models.FloatField(default=0.25)
  planQualifiedRate = models.FloatField(default=0.67)
  closeQuestionRate = models.FloatField(default=0.8)
  autoStartCountdown = models.IntegerField(default=0)
  AgreeRate = models.FloatField(default=0.7)

  # end method and criteria
  endMethod = models.CharField(max_length=1,choices=START_END_METHODS, default='1')
  duration = models.IntegerField(default=0)
  voteRate = models.FloatField(default=0.6)
  autoEndCountdown = models.IntegerField(default=0)
  
  # approach
  voteMethod = models.CharField(max_length=1, choices=VOTE_METHODS, default='1')

  # how many plans one can choose
  maxChoiceCount = models.IntegerField(default=3)

  # other options
  mute = models.BooleanField(default=False) # open discussion / 可否討論留言
  disclosedBallot = models.BooleanField(default=True) # disclosed / 記名投票
  allowAnonymous = models.BooleanField(default=False) # 未登入可投票
  allowNullTicket = models.BooleanField(default=True) # allow invalid/null ticket / 允許廢票
  validCriteria = models.BooleanField(default=True) # valid vote with enough ballot / 表决有效之條件投票率
  newPlanFromAll = models.BooleanField(default=False)

  invalidNullTickRate = models.FloatField(default=0.2) # 廢票率門檻
  validVoteRate = models.FloatField(default=0.6) # 有效投票率

class DonableModel(models.Model):
  karma = models.ManyToManyField(Karma,blank=True)
  discuss = models.ManyToManyField(Discuss,blank=True)
  vote = models.ManyToManyField(Vote,blank=True)

class Proposal(DonableModel):
  owner = models.ForeignKey('auth.User', related_name="proposal")

  title = models.CharField(max_length=100)
  desc = models.TextField(blank=True)

class Ballot(models.Model):
  owner = models.ForeignKey('auth.User', related_name="ballot")
  plan = models.ForeignKey('Plan', related_name="ticket")
  vote = models.ForeignKey('Vote', related_name="ticket")
