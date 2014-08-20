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
  owner = models.ForeignKey('auth.User', related_name="owngroup")
  name = models.CharField(max_length = "100", blank=False)
  desc = models.TextField(blank=True)
  avatar = models.ImageField(upload_to='avatar/g/')
  dept = models.ManyToManyField('self',blank=True)
  karma = models.ManyToManyField(Karma,blank=True)
  discuss = models.ManyToManyField(Discuss,blank=True)
  vote = models.ManyToManyField(Vote, blank=True)
  staff = models.ManyToManyField(User, blank=True, related_name="staff")
  member = models.ManyToManyField(User, blank=True, related_name="member")
  def __unicode__(self):
    return "Group: " + self.name

class UserProfile(models.Model):
  owner = models.ForeignKey('auth.User', related_name="profile")
  group = models.ManyToManyField(WorkGroup)
  def __unicode__(self):
    return self.owner.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(owner=u)[0])
