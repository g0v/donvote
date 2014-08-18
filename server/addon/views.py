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


#-*- coding: utf-8 -*-
import re
import sys
if sys.version < '3':
    text_type = unicode
else:
    text_type = str

from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django_js_reverse.settings import JS_VAR_NAME


def urls_js(request):
    if not re.match(r'^[$A-Z_][\dA-Z_$]*$', JS_VAR_NAME.upper()):
        raise ImproperlyConfigured(
            'JS_REVERSE_JS_VAR_NAME setting "%s" is not a valid javascript identifier.' % (JS_VAR_NAME))

    url_patterns = list(urlresolvers.get_resolver(None).reverse_dict.items())
    url_list = [(url_name, url_pattern[0][0]) for url_name, url_pattern in url_patterns if
                (isinstance(url_name, str) or isinstance(url_name, text_type))]

    return render_to_response('addon/angular_urls_js.tpl',
                              {
                                  'urls': url_list,
                                  'url_prefix': urlresolvers.get_script_prefix(),
                                  'js_var_name': JS_VAR_NAME
                              },
                              context_instance=RequestContext(request), mimetype='application/javascript')

