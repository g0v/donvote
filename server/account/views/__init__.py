from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.core.urlresolvers import reverse
from rest_framework import generics, permissions
from ..models import UserProfile, WorkGroup
from ..serializers import UserProfileSerializer, WorkGroupSerializer
from addon.permissions import IsOwnerOrReadOnly
from addon.views import SubView
from vote.views import DiscussList, VoteList

from . import group, user
