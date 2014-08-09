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


def testAPI(request):
    """
    
    Arguments:
    - `request`:
    """
    ipstr = request.GET.get('ip',None)
    result_str = ""
    if ipstr != None:
        result = _getDianpingDealsByIP(ipstr)

        if result != None:
            for deal in result['deals']:
                result_str += "<h1>" + deal['title'] + "</h1>"
                result_str += "<hr/>" + deal['description']
                result_str += "<hr/>" + str(deal['list_price'])
                result_str += "<hr/>" + str(deal['current_price'])
                result_str += "<hr/>" + deal['image_url']
                result_str += "<hr/>"

    return render_to_response(
        'test/testapi.html',
        {'result':result_str},
        context_instance=RC(request, {}),
    )



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
        #gpons = utils.convert(gpons)
        return gpons
    except Exception as ex:
        print ex
        return None

    
def page(request):
    return render_to_response(
        'configure/index.html',
        {},
        context_instance=RC(request, {}),
    )
    

