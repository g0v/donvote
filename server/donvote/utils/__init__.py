import datetime
from datetime import tzinfo
from datetime import timedelta

class GMT8(tzinfo):
  def utcoffset(self, dt):
    return timedelta(hours=8,minutes=0)
  def tzname(self, dt):
    return "GMT +8"
  def dst(self, dt):
    return timedelta(0)
