
from django.conf.urls import patterns, include, url

from django.contrib import admin

import views

urlpatterns = patterns('',
    url(r'^index/', views.index, name='index' ),
    url(r'^configure/', views.configure, name="configure"),
    url(r'^register/', views.configure, name="register"),
    url(r'^createPageID/', views.createPageID, name="createPageID"),
    url(r'^login/', views.login, name="login"),
    url(r'^testapi/', views.testAPI, name="testapi"),
)
