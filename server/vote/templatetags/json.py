from django import template
from ..serializers import VoteSerializer
from rest_framework.renderers import JSONRenderer
import importlib


register = template.Library()

@register.filter
def dumps(value,arg):
  print(arg)
  print(type(value))
  v = VoteSerializer(value)
  v.is_valid()
  return JSONRenderer().render(v.data)

class commentNode(template.Node):
  def __init__(self, value):
    self.value = valu
  def render(self, context):
    return "/* %s */"%self.value

class resInitNode(template.Node):
  def __init__(self, serializer, args):
    self.serializer = serializer
    self.args = args

  def render(self, context):
    request = context["request"]

    try:
      names = self.args[1].split(".")
      value = context[names[0]]
      for n in names[1:]: value = getattr(value, n)
      v = self.serializer(value)
    except:
      print("no no "+self.args[1])
      return ""

    return ( "<script type='text/javascript'>angular.module('ld.common')" +
           ".config(function(resInitProvider) {" + 
           "  res = resInitProvider.$get();" +
           ("  res['%s'] = %s;"%(self.args[1], JSONRenderer().render(v.data)) ) +
           "});</script>"
           )

cache = {}
@register.tag
def resInit(parser, token):
  args = token.split_contents()
  name = "%s.%s"%(args[2], args[3])
  serializer = cache.get(name, None)
  if serializer == -1: return commentNode("%s not found"%name)
  elif not serializer:
    try:
      serializer = getattr(__import__(args[2], fromlist = [args[3]]), args[3])
      cache[name] = serializer
    except:
      cache[name] = -1
      return commentNode("%s not found"%name)
  return resInitNode(serializer, args)
