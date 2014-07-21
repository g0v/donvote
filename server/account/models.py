from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class WorkGroup(models.Model):
  name = models.CharField(max_length=100, blank=False)
  desc = models.CharField(max_length=200, blank=True)

class UserProfile(models.Model):
  owner = models.ForeignKey('auth.User', related_name="profile")
  group = models.ManyToManyField(WorkGroup)
  def __unicode__(self):
    return self.owner.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(owner=u)[0])

