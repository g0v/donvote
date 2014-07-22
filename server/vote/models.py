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
  planCount = models.IntegerField(default=3)
  needKarma = models.BooleanField(default=False) # 方案 Karma 至少要多少
  karmaRate = models.FloatField(default=0.25)
  karmaCount = models.IntegerField(default=10)
  needQuality = models.BooleanField(default=False) # 多少方案的 Karma 要足夠
  QualifiedRate = models.FloatField(default=0.67)
  needAgree = models.BooleanField(default=False) # 需要大家同意開始
  AgreeRate = models.FloatField(default=0.7)
  needAnswer = models.BooleanField(default=False) # 問題需要回答
  answerRate = models.FloatField(default=0.8)
  needStartCountDown = models.BooleanField(default=False) # 開始前要倒數
  startCountDown = models.IntegerField(default=0)

  # end method and criteria
  endMethod = models.CharField(max_length=1,choices=START_END_METHODS, default='1')
  endDate = models.DateTimeField(blank=True,null=True)
  endByDuration = models.BooleanField(default=False) # 以時間長度來算結束時間
  duration = models.IntegerField(default=0) # 投票期間的時間長度
  needVote = models.BooleanField(default=False) # 投票率要夠高
  voteRate = models.FloatField(default=0.6)
  needEndCountDown = models.BooleanField(default=False) # 結束前要倒數
  endCountDown = models.IntegerField(default=0)
  
  # approach
  voteMethod = models.CharField(max_length=1, choices=VOTE_METHODS, default='1')
  maxChoiceCount = models.IntegerField(default=3)
  rankMethod = models.CharField(max_length=1,choices=RANK_ALGORITHM, default='1')

  # cowork options
  mute = models.BooleanField(default=False) # open discussion / 可否討論留言
  noKarma = models.BooleanField(default=False) # 關閉評價系統
  allowFork = models.BooleanField(default=True) # 允許 fork 此投票案
  allowNewPlan = models.BooleanField(default=False)

  # voting options
  noProxy = models.BooleanField(default=False) # 不允許委任投票, 須親自投票
  disclosedBallot = models.BooleanField(default=True) # disclosed / 記名投票
  allowAnonymous = models.BooleanField(default=False) # 未登入可投票

  # valid vote option
  allowNullTicket = models.BooleanField(default=True) # 允許廢票
  useNullTicketRate = models.BooleanField(default=False) # 廢票過高時投票無效
  nullTickRate = models.FloatField(default=0.2) # 廢票率門檻
  useValidVoteRate = models.BooleanField(default=True) # valid vote with enough ballot / 表决有效之條件投票率
  validVoteRate = models.FloatField(default=0.6) # 有效投票率
  useObtainRate = models.BooleanField(default=False) # 最高得票率需高於一定門檻
  ObtainRate = models.FloatField(default=0.3)

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
