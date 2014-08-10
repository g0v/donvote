from rest_framework import generics
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from ..permissions import IsOwnerOrReadOnly, VotePermission, PlanPermission
from ..serializers import VoteSerializer, PlanSerializer, DiscussSerializer, KarmaSerializer, BallotSerializer
from ..models import Vote, Plan, Discuss, Karma, Ballot
from django.views.generic import TemplateView, View
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseNotFound, Http404

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
  def pre_save(self, obj):
    obj.owner = self.request.user

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
    context['vote'] = vote[0] if len(vote) else None
    return context

class VoteListPage(TemplateView):
  template_name = "vote/list.jade"
  def get_context_data(self, **kwargs):
    context = super(VoteListPage, self).get_context_data(**kwargs)
    vote = Vote.objects.all()
    context['votes'] = vote
    return context

# attempt to build vote-sub-discuss api
def SubView(o_class):
  o_get_queryset = o_class.get_queryset
  o_pre_delete = o_class.pre_delete
  o_post_save = o_class.pre_save

  root_class = None
  target_field = ""

  # need to check if obj exists
  def get_queryset(self):
    obj = self.root_class.objects.filter(pk=self.kwargs[self.target_field+"_owner_pk"])
    if len(obj): return obj[0].__getattribute__(self.target_field).all()
    else: return []
  def pre_delete(self, obj):
    obj = self.root_class.objects.filter(pk=self.kwargs[self.target_field+"_owner_pk"])
    if len(obj): obj[0].__getattribute__(self.target_field).remove(obj)
    super(o_class, self).pre_delete(obj)
  def post_save(self, obj, created=False):
    v = self.root_class.objects.filter(pk=self.kwargs[self.target_field+"_owner_pk"])
    if len(v): v[0].__getattribute__(self.target_field).add(obj)
    super(o_class, self).post_save(obj)

  o_class.get_queryset = get_queryset
  o_class.pre_delete = pre_delete
  o_class.post_save = post_save
  return o_class

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
    return map(lambda x: x[0] if len(x) else None, [v,p,b])

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
