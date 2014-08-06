# -*- coding: utf-8 -*-
from django.db import models
from donvote import utils
from datetime import datetime
from donvote.utils import GMT8
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
  plan = models.ManyToManyField(Plan,blank=True)
  ongoing = models.BooleanField(default=False)

  START_END_METHODS = (
      ('1', 'manually'),
      ('2', 'time'),
      ('3', 'criteria'),
  )

  VOTE_METHODS = (
      ('1', 'single'),
      ('2', 'multiple'),
      ('3', 'ranking'),
      ('4', 'scoring'),
  )

  RANK_ALGORITHM = (
      ('1', 'Schulze Method'),
  )

  # start method and criteria
  startMethod = models.CharField(max_length=1,choices=START_END_METHODS, default='1')
  startDate = models.DateTimeField(blank=True,null=True)
  needPlan = models.BooleanField(default=False) # 至少要有多少方案
  planCount = models.IntegerField(default=2)
  needKarma = models.BooleanField(default=False) # 方案 Karma 至少要多少
  karmaRate = models.FloatField(default=10.0)
  karmaCount = models.IntegerField(default=10)
  needQuality = models.BooleanField(default=False) # 多少方案的 Karma 要足夠
  qualifiedRate = models.FloatField(default=25)
  needAgree = models.BooleanField(default=False) # 需要大家同意開始
  agreeRate = models.FloatField(default=20)
  needAnswer = models.BooleanField(default=False) # 問題需要回答
  answerRate = models.FloatField(default=70)
  needStartCountDown = models.BooleanField(default=False) # 開始前要倒數
  startCountDown = models.IntegerField(default=0)

  # end method and criteria
  endMethod = models.CharField(max_length=1,choices=START_END_METHODS, default='1')
  endDate = models.DateTimeField(blank=True,null=True)
  endByDuration = models.BooleanField(default=False) # 以時間長度來算結束時間
  duration = models.IntegerField(default=0) # 投票期間的時間長度
  needVote = models.BooleanField(default=False) # 投票率要夠高
  voteRate = models.FloatField(default=75)
  needEndCountDown = models.BooleanField(default=False) # 結束前要倒數
  endCountDown = models.IntegerField(default=0)
  
  # approach
  voteMethod = models.CharField(max_length=1, choices=VOTE_METHODS, default='1')
  maxChoiceCount = models.IntegerField(default=2)
  rankMethod = models.CharField(max_length=1,choices=RANK_ALGORITHM, default='1')

  # cowork options
  mute = models.BooleanField(default=False) # open discussion / 可否討論留言
  noKarma = models.BooleanField(default=False) # 關閉評價系統
  allowFork = models.BooleanField(default=True) # 允許 fork 此投票案
  allowNewPlan = models.BooleanField(default=False)

  # voting options
  noProxy = models.BooleanField(default=False) # 不允許委任投票, 須親自投票
  disclosedBallot = models.BooleanField(default=False) # disclosed / 不記名投票
  allowAnonymous = models.BooleanField(default=False) # 未登入可投票

  # valid vote option
  allowNullTicket = models.BooleanField(default=True) # 允許廢票
  useNullTicketRate = models.BooleanField(default=False) # 廢票過高時投票無效
  nullTicketRate = models.FloatField(default=40) # 廢票率門檻
  useValidVoteRate = models.BooleanField(default=True) # valid vote with enough ballot / 表决有效之條件投票率
  validVoteRate = models.FloatField(default=66) # 有效投票率
  useObtainRate = models.BooleanField(default=False) # 最高得票率需高於一定門檻
  obtainRate = models.FloatField(default=30)

  @property
  def isOngoing(self):
    now = datetime.now(GMT8())
    if self.startMethod == '1': return self.ongoing
    elif self.startMethod == '2': 
      if now < self.startDate: return False
      if self.endMethod == '1': return True
      elif self.endMethod == '2':
        if now >= self.endDate: return False
      elif self.endMethod == '3': return False # TODO
    elif self.startMethod == '3': return False # TODO
    return False
  @property
  def getPlanCount(self):
    return len(self.plan.all())

class DonableModel(models.Model):
  karma = models.ManyToManyField(Karma,blank=True)
  discuss = models.ManyToManyField(Discuss,blank=True)
  vote = models.ManyToManyField(Vote,blank=True)

class Proposal(DonableModel):
  owner = models.ForeignKey('auth.User', related_name="proposal")

  title = models.CharField(max_length=100)
  desc = models.TextField(blank=True)

class Ballot(WithDateModel):
  owner = models.ForeignKey('auth.User', related_name="ballot")
  plan = models.ForeignKey('Plan', related_name="ballot", blank=True, null=True)
  vote = models.ForeignKey('Vote', related_name="ballot")
  value = models.PositiveIntegerField(default=0)
