from django import template
from rest_framework.renderers import JSONRenderer
from django.core.urlresolvers import reverse
import importlib, string

register = template.Library()

class urlPatternNode(template.Node):
  def render(self, context):
    return """<script type="text/javascript" src="%s"></script>"""%(reverse("reversejs"))

@register.tag
def urlpatterns(parser, token):
  return urlPatternNode()

@register.filter
def aj(value):
    return "{{%s}}" % str(value)

@register.filter
def dumps(value,arg):
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
      return ""

    return ( "<script type='text/javascript'>angular.module('django.common')" +
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

class resInitAllNode(template.Node):
  def render(self, context):
    
    core = []
    for item in context["resInit"]:
      name = item["name"]
      data = JSONRenderer().render(item["serializer"](item["obj"]).data)
      core = core + ["  res['%s'] = %s;"%(name, data)]

    core = [
      "<script type='text/javascript'>angular.module('django.common')",
      ".config(function(resInitProvider) {",
      "  res = resInitProvider.$get();"
    ] + core + [
      "});</script>"
    ]
    return string.join(core, "\n")


@register.tag
def resInitAll(parser, token):
  return resInitAllNode()
