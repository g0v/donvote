# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import ast

# read_only field in every class means:
# from_native 是否有機會被跑到

class CountRelatedField(serializers.RelatedField):
  read_only = True
  def field_to_native(self, obj, field_name):
    field = getattr(obj, field_name)
    return len(field.all())

class DetailRelatedField(serializers.RelatedField):
  def to_native(self, value):
    obj = self.serializer(value)
    return obj.data

  def to_object(self, data):
    if type(data)!=type({}):
      try: data = ast.literal_eval(data)
      except: raise ValidationError(self.error_messages["invalid"])
    try:
      obj = self.queryset.get(id=(data.get("id") or -1))
      return [data, obj]
    except: pass
    return [data, None]

  def from_native(self, data):
    [data,obj] = self.to_object(data)
    if not obj: raise ObjectDoesNotExist("")
    return obj

class WritableDetailRelatedField(DetailRelatedField):
  read_only = False
  def from_native(self, data):
    [data,obj] = self.to_object(data)
    if obj: return obj
    obj = self.serializer(data=data)
    if not obj.is_valid(): raise ValidationError(self.error_messages["invalid"])
    obj.object.owner = self.context["request"].user
    obj.object.save()
    return obj.object
