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
import models


def index(request):
    return HttpResponse("hello, world!")


@login_required(login_url='/api/login/')
def configure(request):
    """
    
    Arguments:
    - `request`:
    """
    response_data = {}
    response_data['status'] = 'yes'

    if request.method != 'POST':
            response_data['status'] = 'no'
            response_data['error'] = 'This api only support POST call!'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        

    page_id = request.POST.get('page_id', None)
    configure_id = request.POST.get('configure_id', None)
    if page_id != None:
        if configure_id == None:
            #create a new one
            c = models.ConfigEntity(page = page_id,
                                    black_list = '',
                                    white_list = '',
                                    traffic_percentage = 0,
                                    bidding_approach = 0,
                                    layout_option = 0)
            c.save()

        else:
            try:
                c = models.ConfigEntity.objects.get(page = page_id)

                traffic_percentage = request.POST.get('traffic',None)
                white_list = request.POST.get('white_list',None)
                black_list = request.POST.get('black_list',None)
                bidding_approach = request.POST.get('bidding',None)
                layout_option = request.POST.get('layout',None)
                #parameter condition check            
                if traffic_percentage != None:
                    c.traffic_percentage = traffic_percentage
                if white_list != None:
                    c.white_list = white_list
                if black_list != None:
                    c.black_list = black_list
                if bidding_approach != None:
                    c.bidding_approach = bidding_approach
                if layout_option != None:
                    c.layout_approach = layout_option

                c.save()
            except Exception as inst:
                #doesn't exist such configure for this page, return error code to client
                response_data['status'] = 'no'
                response_data['error']  = str(inst)
    else:
        response_data['status'] = 'no'
        response_data['error'] = 'Page id must be assigned!'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


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
    

