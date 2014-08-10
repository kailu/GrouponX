
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

import views


class DirectTemplateView(TemplateView):
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        if self.extra_context is not None:
            for key, value in self.extra_context.items():
                if callable(value):
                    context[key] = value()
                else:
                    context[key] = value
        return context


urlpatterns = patterns('',
    # redirect / to index.html
    url(r'^$', DirectTemplateView.as_view(template_name='index.html')),

    url(r'^index/', views.index, name='index'),
    url(r'^configure/', views.configure, name="configure"),
    url(r'^createPageID', views.createPageID, name="createPageID"),

    url(r'^login/', views.login_, name="login"),
    url(r'^logout/', views.logout_, name="logout"),
    url(r'^register/', views.register, name="register"),
    url(r'^pwd_reset/', views.pwd_reset, name="pwd_reset"),
    url(r'^testapi/', views.testAPI, name="testapi"),
    url(r'^page/',views.page, name="page"),
    url(r'^getdeals', views.getdeals, name='getdeals'),
    url(r'^createpage',views.createPage, name='createpage'),
    url(r'^readpage$', views.readPage, name='readpage'),
    url(r'^savepage$', views.savePage, name='savepage'),
    url(r'^readpagelist$', views.readPageList, name='readpagelist'),
    url(r'^createconfig', views.createConfigure, name='createconfig'),
    url(r'^readconfig', views.readConfigure, name='readconfig'),
    url(r'^saveconfig', views.saveConfigure, name='saveconfig'),
    url(r'^serving$',views.serving, name='serving'),
    url(r'^admin/', include(admin.site.urls)),
)
