from django.contrib import admin
from . import models
import inspect

# Register your models here.
admin.site.register(
  filter(lambda x: x.__module__.startswith("vote"),
    map(lambda x: x[1], (inspect.getmembers(models, inspect.isclass)))
))
