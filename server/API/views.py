# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

import baidu
import dianping
import utils
import json

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
    """
    
    Arguments:
    - `request`:
    """
    pass


@login_required(login_url='/api/login/')
def createPageID(request):
    """
    
    Arguments:
    - `request`:
    """
    pass


def testAPI(request):
    """
    
    Arguments:
    - `request`:
    """
    ipstr = request.GET.get('ip',None)
    result = _getDianpingDealsByIP(ipstr)
    result_str = ""
    if result != None:
        for deal in result['deals']:
            result_str += "<hr/>" + deal['title']
            result_str += "<hr/>" + deal['image_url']
            result_str += "<hr/>"

    return HttpResponse(result_str)


def _getDianpingDealsByIP(ipstr):
    """
    
    Arguments:
    - `ipstr`:
    """
    d = baidu.getAddressByIP(ipstr)
    try:
        d = json.loads(d)
        city = d['content']['address_detail']['city']


        if city.endswith(u"市"):
            city = city[:-1]
        city = city.encode('utf-8')
        #call dianping API
        gpons = dianping.getGrouponByCity(city)
        gpons =  utils.convert(gpons)
        return gpons
    except Exception as ex:
        print ex
        return None

    


