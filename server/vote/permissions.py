from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Vote

class PlanPermission(permissions.BasePermission):
  def has_permission(self, request, view):
    return True

class VotePermission(permissions.BasePermission):
  def compare(self, src, des):
    src = map(lambda x: x.id, src)
    des = map(lambda x: x.get("id") or -1, des)
    for item in des: 
      if not (item in src): return False
    return True

  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    if request.user == obj.owner: return True
    for k in request.DATA:
      try: src = getattr(obj,k)
      except: continue
      des = request.DATA[k]
      if type(src) == User:
        result = True if src.username==des else False
      elif str(type(src)).startswith("<class 'django.db.models.fields.related.ManyRelatedManager'>"):
        result = self.compare(src.all(), des)
      else: result = (src==des)
      if k=="plan" and not result and (obj.newPlanFromAll or request.user==obj.owner): continue
      if k=="discuss" and not result and not obj.mute: continue
      elif k in ["createDate","modifyDate"]: continue
      elif not result: return False
    return True
