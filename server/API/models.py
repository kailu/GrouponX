from django.db import models

# Create your models here.


from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class PageEntity(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    pagename = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now = True)

#
# Bidding number mapping:
# 1 --- location first
# 2 --- max discount first
# 3 --- cheapest price first
#
# layout mapping:
# 1 --- template 1
# 2 --- tempate 2
class ConfigEntity(models.Model):
    page = models.ForeignKey(PageEntity)
    black_list = models.CharField(max_length=1024)
    white_list = models.CharField(max_length=1024)
    traffic_percentage = models.FloatField(default = 1)
    bidding_approach = models.IntegerField()
    layout_approach = models.IntegerField()
    created_at = models.DateTimeField(auto_now = True)


        
