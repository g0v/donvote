# -*- coding: utf-8 -*-
from django.db import models
from donvote import utils
from datetime import datetime, timedelta
from donvote.utils import GMT8
from django.contrib.auth.models import User, Group

# Create your models here.

# TODO try use class decorator
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
  tendency = models.IntegerField(default=2)
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

  # 投票是否進行中 - 手動開始/結束投票時專用
  # 0 - 還沒開始; 1 - 已經開始, 尚未結束; 2 - 已經結束
  ONGOING_VALUE = (
      ('0','not start'),
      ('1','countdown to start'),
      ('2','ongoing'),
      ('3','countdown to end'),
      ('4','ended'),
  )
  onGoingManually = models.CharField(max_length=1, choices=ONGOING_VALUE, default='0')

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
  startCountDownDate = models.DateTimeField(blank=True,null=True) # 滿足條件後開始'開始倒數'的時間
  needPlan = models.BooleanField(default=False) # 至少要有多少方案
  planCount = models.IntegerField(default=2)
  needKarmaRate = models.BooleanField(default=False) # 方案 Karma 至少要多少 (比例)
  karmaRate = models.FloatField(default=10.0)
  needKarmaCount = models.BooleanField(default=False) # 方案 Karma 至少要多少 (數量)
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
  endCountDownDate = models.DateTimeField(blank=True,null=True) # 滿足條件後開始'結束倒數'的時間
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

  def timedelta(value):
    value = int(( value - (value % 60) ) / 60)
    minute = value % 60
    hour = int(((value % 1440) - (value % 60)) / 60)
    day = int((value - (value % 1440)) / 1440)
    return timedelta(day, 0, 0, 0, minute, hour)

  def totalVoterCount(self):
    return 10 #TODO: implement this

  def setOnGoing(self, value, countdown = False):
    old_value = self.onGoingManually
    self.onGoingManually = value
    if old_value != self.onGoingManually: self.save()
    return value

  @property
  def isOnGoing(self):
    now = datetime.now(tz = GMT8())
    if self.onGoingManually == '4': return '4'
    if self.onGoingManually == '0' or self.onGoingManually == '1':
      if self.startMethod == '1': return self.onGoingManually
      if self.startMethod == '2' and now >= self.startDate: self.setOnGoing('2')
      if self.startMethod == '3':
        # retun setOnGoing('0') for reset countdown
        if self.needPlan and len(self.plan.all()) < self.planCount: return setOnGoing('0')
        if self.needQuality: # issue: need optimization!
          plans = self.plan.all()
          count = 0
          total = len(plans)
          for plan in plans:
            valid = True
            if self.needKarmaCount and len(plan.karma.all()) < self.karmaCount: valid = False
            if self.needKarmaRate and len(plan.karma.all()) < self.karmaRate: valid = False
            if valid: count+=1
          if total==0 or count / total < self.qualifiedRate / 100: return setOnGoing('0')
        if self.needAgree:
          count = 0 # TODO: add agree table
          if count / self.totalVoterCount() < self.agreeRate / 100: return setOnGoing('0')
        if self.needAnswer:
          # TODO: add answer mechanism
          return setOnGoing('0')
        # all criteria passed. modify vote ongoing state
        if self.needStartCountDown:
          if self.onGoingManually == '0': self.startCountDownDate = now
          if self.onGoingManually == '1' and now >= self.startCountDownDate + timedelta(0,self.startCountDown): return setOnGoing('2')
          return self.setOnGoing('1')
        return self.setOnGoing('2')
    if self.onGoingManually == '2' or self.onGoingManually == '3':
      if self.endMethod == '1': return '2'
      if self.endMethod == '2' and now >= self.endDate: return self.setOnGoing('4')
      if self.endMethod == '3':
        if self.needVote:
          ballot = self.ballot.all()
          if len(ballot) / self.totalVoterCount() < self.voteRate / 100: return setOnGoing('2')

        # all criteria passed. modify vote ongoing state
        if self.needEndCountDown:
          if self.onGoingManually == '2': self.endCountDownDate = now
          if self.onGoingManually == '3' and now >= self.endCountDownDate + timedelta(0,self.endCountDown): return setOnGoing('4')
          return self.setOnGoing('3')
        return self.setOnGoing('4')
    return self.onGoingManually

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
