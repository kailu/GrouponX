# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext as RC

from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

import baidu
import dianping


def index(request):
    return HttpResponse("hello, world!")


@login_required(login_url='/api/login/')
def configure(request):
    """
    
    Arguments:
    - `request`:
    """
    pass


def register(request):
    """
    
    Arguments:
    - `request`:
    """
    pass


def login(request):
    return render_to_response(
        'registration/login.html',
        {},
        context_instance=RC(request, {}),
    )


def register(request):
    return render_to_response(
        'registration/registration_form.html',
        {},
        context_instance=RC(request, {}),
    )


def pwd_reset(request):
    return render_to_response(
        'registration/pwd_reset_form.html',
        {},
        context_instance=RC(request, {}),
    )


@login_required(login_url='/api/login/')
def createPageID(request):
    """
    
    Arguments:
    - `request`:
    """
    pass


def _getDianpingDealsByIP(ipstr):
    """
    
    Arguments:
    - `ipstr`:
    """
    d = baidu.getAddressByIP(ipstr)
    try:
        city = d['content']['address_detail']['city']
        if city.endswith("\u市"):
            city = city[:-1]
        city = city.encode('utf-8')
        #call dianping API
        gpons = dianping.getGrouponByCity(city)
        #gpons = utils.convert(gpons)
        return gpons
    except:
        return None

    


