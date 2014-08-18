# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.contrib.auth.models import User
from account.models import UserProfile, WorkGroup, NameList
site = Site.objects.all()[0]
site.domain = "localhost:8002"
site.name = "localhost:8002"
site.save()

app = SocialApp.objects.create()
app.provider = 'facebook'
app.name = 'facebook'
app.client_id = '836557763029341'
app.secret = '807d0b80b25fb43a0318984e4cf39087'
app.sites.add(site)
app.save()

from vote.models import Vote, Plan, Discuss

admin = User.objects.filter(username="admin")[0]
vote = Vote.objects.create(name="測試用提案", desc="就只是測試",owner=admin)
p1 = vote.plan.create(name="贊成", desc="我支持",owner=admin)
p2 = vote.plan.create(name="反對", desc="我不同意",owner=admin)
p3 = vote.plan.create(name="中立", desc="我沒有意見",owner=admin)
d1 = vote.discuss.create(content="這只是一個測試用的投票案",owner=admin)
p1.owner = admin
p2.owner = admin
p3.owner = admin
d1.owner = admin

vote.save()
p1.save()
p2.save()
p3.save()
d1.save()

n = NameList.objects.create(name="組名單",owner=admin)
n.user.add(admin)
n.save()
w = WorkGroup.objects.create(name="測試組",desc="這是一個測試用的群組",members=n)
d2 = w.discuss.create(content="測試群組中的一個測試留言", owner=admin)
d2.save()
w.vote.add(vote)
w.save()

adminProfile = admin.profile
tkirby = User.objects.create(username="tkirby")
tkirbyProfile = tkirby.profile
