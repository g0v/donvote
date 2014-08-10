from django.db import models
from django.contrib.auth.models import User
from vote.models import Karma, Discuss, Vote

# Create your models here.

class NameList(models.Model):
  owner = models.ForeignKey('auth.User', related_name="namelist")
  name = models.CharField(max_length = "100",blank=False)
  desc = models.TextField(blank=True)
  user = models.ManyToManyField(User, related_name="inlist")

class WorkGroup(models.Model):
  name = models.CharField(max_length = "100", blank=False)
  desc = models.TextField(blank=True)
  dep = models.ManyToManyField('self')
  karma = models.ManyToManyField(Karma,blank=True)
  discuss = models.ManyToManyField(Discuss,blank=True)
  vote = models.ManyToManyField(Vote, blank=True)
  members = models.ForeignKey(NameList, related_name = "workgroup")
  def __unicode__(self):
    return "Group: " + self.name

class UserProfile(models.Model):
  owner = models.ForeignKey('auth.User', related_name="profile")
  group = models.ManyToManyField(WorkGroup)
  def __unicode__(self):
    return self.owner.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(owner=u)[0])

