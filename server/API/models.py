from django.db import models
from django.contrib.auth.forms import UserCreationForm

# Create your models here.


from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from django.contrib import admin

class RegistrationForm(UserCreationForm):
    domain = forms.CharField(max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(RegistrationForm, self).save(commit=True)
        return user


class Site(models.Model):
    user = models.OneToOneField(User)
    domain = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)

class SiteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Site, SiteAdmin)


class PageEntity(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    pagename = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now = True)

class PageAdmin(admin.ModelAdmin):
    pass

admin.site.register(PageEntity, PageAdmin)

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
    name = models.CharField(max_length=100)
    black_list = models.CharField(max_length=1024)
    white_list = models.CharField(max_length=1024)
    traffic_percentage = models.FloatField(default = 1)
    bidding_approach = models.IntegerField()
    layout_approach = models.IntegerField()
    created_at = models.DateTimeField(auto_now = True)


        
class ConfigAdmin(admin.ModelAdmin):
    pass

admin.site.register(ConfigEntity, ConfigAdmin)

