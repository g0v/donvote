from rest_framework import generics
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from ..permissions import VotePermission, PlanPermission
from ..serializers import VoteSerializer, PlanSerializer, DiscussSerializer, KarmaSerializer, BallotSerializer
from ..models import Vote, Plan, Discuss, Karma, Ballot
from django.views.generic import TemplateView, View
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseNotFound, Http404
from addon.views import SubView
from addon.permissions import IsOwnerOrReadOnly

class PlanList(generics.ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly)
  queryset = Plan.objects.all()
  serializer_class = PlanSerializer
  def pre_save(self, obj):
    obj.owner = self.request.user

class PlanDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
  queryset = Plan.objects.all()
  serializer_class = PlanSerializer
  def pre_save(self, obj):
    obj.owner = self.request.user

class BallotList(generics.ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly)
  queryset = Ballot.objects.all()
  serializer_class = BallotSerializer
  def pre_save(self, obj):
    obj.owner = self.request.user

class VoteList(generics.ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
  queryset = Vote.objects.all()
  serializer_class = VoteSerializer
  def pre_save(self, obj):
    if not obj.owner_id: obj.owner = self.request.user

class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,VotePermission)
  queryset = Vote.objects.all()
  serializer_class = VoteSerializer
  def pre_save(self, obj):
    if not obj.owner_id: obj.owner = self.request.user


class KarmaList(generics.ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
  queryset = Discuss.objects.all()
  serializer_class = KarmaSerializer
  root_class = None
  def pre_save(self, obj):
    obj.owner = self.request.user

  def post(self, request, *args, **kargs):
    d = root_class.objects.filter(pk=self.kwargs.get("karma_owner_pk") or -1)
    if len(d)==0: return HttpResponseNotFound()
    k = d.karma.filter(owner=request.user)
    if len(k) == 0:
      k = KarmaSerializer(data=request.DATA)
    else:
      k = KarmaSerializer(k[0], data=request.DATA)
    if not k.is_valid(): return HttpResponseNotAllowed("data validation failed")
    k.save()
    d.karma.add(k)
    return super(DiscussSubKarmalist, self).post(request, *args, **kwargs)

class DiscussList(generics.ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
  queryset = Discuss.objects.all()
  serializer_class = DiscussSerializer
  def pre_save(self, obj):
    obj.owner = self.request.user

class DiscussDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
  queryset = Discuss.objects.all()
  serializer_class = DiscussSerializer
  def pre_save(self, obj):
    obj.owner = self.request.user

class VoteDetailView(TemplateView):
  template_name = "vote/detail.jade"
  def get_context_data(self, **kwargs):
    context = super(VoteDetailView, self).get_context_data(**kwargs)
    vote = Vote.objects.filter(pk=kwargs['pk'])
    context["vote_json"] = JSONRenderer().render(VoteSerializer(vote[0]).data) if len(vote) else ""
    context['vote'] = vote[0] if len(vote) else None
    return context

class VoteListPage(TemplateView):
  template_name = "vote/list.jade"
  def get_context_data(self, **kwargs):
    context = super(VoteListPage, self).get_context_data(**kwargs)
    vote = Vote.objects.all()
    context['votes'] = vote
    return context

@SubView
class VoteSubDiscussList(DiscussList):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
  root_class = Vote
  target_field = "discuss"
  def post(self, request, *args, **kwargs):
    v = Vote.objects.filter(pk=self.kwargs.get("discuss_owner_pk") or -1)
    if len(v)==0 or v[0].mute: return HttpResponseNotAllowed("Vote is Muted")
    return super(VoteSubDiscussList, self).post(request, *args, **kwargs)

@SubView
class VoteSubKarmaList(KarmaList):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
  root_class = Vote
  target_field = "karma"
  def post(self, request, *args, **kwargs):
    if len(Karma.objects.filter(owner=request.user))>0: return HttpResponseNotAllowed("one Karma per user is allowed")
    v = Vote.objects.filter(pk=self.kwargs.get("discuss_owner_pk") or -1)
    if len(v)==0 or v[0].noKarma: return HttpResponseNotAllowed("karma is turned off")
    return super(VoteSubKarmaList, self).post(request, *args, **kwargs)

@SubView
class VoteSubPlanList(PlanList):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
  root_class = Vote
  target_field = "plan"
  def post(self, request, *args, **kwargs):
    v = Vote.objects.filter(pk=self.kwargs.get("plan_owner_pk") or -1)
    if len(v)==0 or (v[0].owner!=request.user and not v[0].allowNewPlan):
      return HttpResponseNotAllowed("new plan is only allowed from owner")
    return super(VoteSubPlanList, self).post(request, *args, **kwargs)

class BallotView(View):
  def prepare(self, request, *args, **kwargs):
    v = Vote.objects.filter(pk=(kwargs.get("vote_pk") or -1))
    p = Plan.objects.filter(pk=(kwargs.get("plan_pk") or -1))
    b = Ballot.objects.filter(pk=(kwargs.get("ballot_pk") or -1))
    if kwargs.get("ballot_pk") and not b: raise Http404()
    if len(v): all_b = v[0].ballot.filter(pk=(kwargs.get("ballot_pk") or -1))
    return map(lambda x: x[0] if len(x) else None, [v,p,b, all_b])

  def get(self, request, *args, **kwargs):
    objs = self.prepare(request, *args, **kwargs)
    if kwargs.get("ballot_pk"): 
      b = objs[2]
      if not b: return HttpResponseNotFound()
    else:
      b = Ballot.objects.filter(owner=request.user)
      if objs[0]: b = b.filter(vote=objs[0])
      if objs[1]: b = b.filter(plan=objs[1])
    b = BallotSerializer(b)
    return HttpResponse(JSONRenderer().render(b.data),content_type="application/json")

  def post(self, request, *args, **kwargs):
    objs = self.prepare(request, *args, **kwargs)
    if not (objs[0]) or objs[2]: return HttpResponseNotAllowed("ambiguous/duplicate ballot")
    if objs[3]>1 and objs[0].voteMethod=='1': return HttpResponseNoteAllowed("only one ballot allowed")
    ret = Ballot.objects.filter(owner=request.user).filter(vote=objs[0]).filter(plan=objs[1])
    if len(ret): return HttpResponseNotAllowed("duplicate ballot")
    b = Ballot.objects.create(vote=objs[0],plan=objs[1],owner=request.user,value=0)
    return HttpResponse()

  def delete(self, request, *args, **kwargs): 
    objs = self.prepare(request, *args, **kwargs)
    if objs[2]: objs[2].delete()
    else:
      b = Ballot.objects.filter(vote=objs[0]).filter(plan=objs[1])
      if len(b)==0: return HttpResponseNotFound()
      else: b[0].delete()
    return HttpResponse()

class VoteSubBallotList(BallotList):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
  root_class = Vote
  target_field = "ballot"
  def post(self, request, *args, **kwargs):
    v = Vote.objects.filter(pk=self.kwargs.get("ballot_owner_pk") or -1)
    if len(v)==0 or (v[0].owner!=request.user and not v[0].allowNewPlan):
      return HttpResponseNotAllowed("new plan is only allowed from owner")
    return super(VoteSubPlanList, self).post(request, *args, **kwargs)

class VoteNewView(TemplateView):
  template_name = "vote/edit.jade"
  def get_context_data(self, **kwargs):
    context = super(VoteDetailView, self).get_context_data(**kwargs)
    vote = Vote.objects.filter(pk=kwargs['pk'])
    context['vote'] = vote[0] if len(vote) else None
    return context

class VoteEditView(TemplateView):
  template_name = "vote/edit.jade"
  def get_context_data(self, **kwargs):
    context = super(VoteEditView, self).get_context_data(**kwargs)
    if not kwargs.get("pk"): return context
    vote = Vote.objects.filter(pk=kwargs['pk'])
    context['vote'] = vote[0] if len(vote) else None
    return context

@SubView
class DiscussSubKarmaList(KarmaList):
  root_class = Discuss
  target_field = "karma"


