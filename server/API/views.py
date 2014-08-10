# -*- coding: utf-8 -*-
from django import conf
from django.contrib.auth import authenticate,login,logout

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext as RC

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from models import RegistrationForm, Site
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
import hashlib

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

import baidu
import dianping
import utils
import json
import models
from django.forms.models import model_to_dict


def index(request):
    return HttpResponse("hello, world!")


def createConfigure(request):
    """
    
    Arguments:
    - `request`:
    """
    response_data = {}
    response_data['status'] = 'ok'
    if request.method == 'GET':
        page_id = request.GET.get('p_id', None)
        config_name = request.GET.get('name', None)

        if page_id == None:
            response_data['status'] = 'no'
            response_data['error'] = 'no page id specified!'
        else:
            p = models.PageEntity.objects.get(pk=page_id)
            c = models.ConfigEntity(page = p,
                                    name = config_name,
                                    black_list = '',
                                    white_list = '',
                                    traffic_percentage = 0,
                                    bidding_approach = 0,
                                    layout_approach = 0)
            c.save()
            response_data['data'] = model_to_dict(c)
            
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def readConfigure(request):
    """
    
    Arguments:
    - `request`:
    """
    response_data = {}
    response_data['status'] = 'ok'
    c_id = request.GET.get('c_id',None)
    if c_id != None:
        try:
            conf = models.ConfigEntity.objects.get(pk = c_id)
            response_data['data'] = model_to_dict(conf)
        except Exception as error:
            response_data['status'] = 'no'
            response_data['error'] = str(error)

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def saveConfigure(request):
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
        

    page_id = request.POST.get('p_id', None)
    configure_id = request.POST.get('c_id', None)
    if page_id != None:
        if configure_id == None:
            #create a new one
            response_data['status'] = 'no'
            response_data['error'] = 'configure id does not exist!'
        else:
            try:
                p = models.PageEntity.objects.get(pk = page_id)
                c = models.ConfigEntity.objects.get(pk = configure_id)
                #if c.page != p:


                traffic_percentage = request.POST.get('traffic',None)
                white_list = request.POST.get('white_list',None)
                black_list = request.POST.get('black_list',None)
                bidding_approach = request.POST.get('bidding_approach',None)
                layout_option = request.POST.get('layout_approach',None)
                name = request.POST.get('name',None)

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
                if name != None:
                    c.name = name

                c.save()
            except Exception as inst:
                #doesn't exist such configure for this page, return error code to client
                response_data['status'] = 'no'
                response_data['error']  = str(inst)
    else:
        response_data['status'] = 'no'
        response_data['error'] = 'Page id must be assigned!'
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    


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


def login_(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        return login_to_page(request, username, password)

    else:
        form = AuthenticationForm()
        return render_to_response(
            'registration/login.html',
            { 'form' : form},
            context_instance=RC(request, {}),
    )


def logout_(request):
    logout(request)
    return render_to_response(
        'index.html',
        {},
        context_instance=RC(request, {}),
    )


def login_to_page(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            print("User is valid, active and authenticated")
            print "domain: ", user.site.domain
            print "u_id", user.id
            return HttpResponseRedirect('../page/')
        else:
            print("The password is valid, but the account has been disabled!")
    else:
        # the authentication system was unable to verify the username and password
        print("The username and password were incorrect.")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        domain = request.POST['domain']
        print "=== User: ", username, " password: ", password, 'domain: ', domain

        new_user = User.objects.create_user(username, '', password)

        # create hash for new user
        hasher = hashlib.md5()
        hasher.update(username + domain)
        h = hasher.hexdigest()
        site = Site(user=new_user, hash=h, domain=domain)
        site.save()
        new_user.save()

        return login_to_page(request, username, password)

    else:
        form = RegistrationForm()
        return render_to_response(
            'registration/registration_form.html',
            {'form' : form},
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

@login_required(login_url='/api/login/')
def createPage(request):
    """
    
    Arguments:
    - `request`:
    """
    response_data = {}
    response_data['status'] = 'ok'
    
    name = request.GET.get('name',None)
    if name == None:
        response_data['status'] = 'no'
        response_data['error'] = 'need a name for page!'
    else:
        page = models.PageEntity(user = request.user,
                                 name = name,
                                 pagename = '')
        page.save()
        d = {}
        d['p_id'] = page.id
        response_data['data'] = d
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#@login_required(login_url='/api/login')
@csrf_exempt
def savePage(request):
    print "--- savePage ---"
    response_data = {}

    if request.method == 'POST':
            """
                {
                    data : [config array],
                    p_id: int
                }
            """
            payload = json.loads(request.body)
            p_id = payload['p_id']
            print 'p_id', p_id

            if isinstance(payload['data'], list):
                for config in payload['data']:
                    print config
                    c = models.ConfigEntity.objects.get(pk=config['id'])
                    c.traffic_percentage = config['traffic_percentage']
                    c.save()
            else:
                print 'data not a list'

    else:
        response_data['status'] = 'fail'
        response_data['reason'] = 'Not a POST call'
        return HttpResponse(json.dumps(response_data), content_type="application/json")


    print 'savePage - ajax post: ', request.body

    response_data['status'] = 'ok'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/api/login/')
def readPage(request):
    """
    
    Arguments:
    - `request`:
    """
    response_data = {}
    response_data['status'] = 'ok'
    p_id = request.GET.get('p_id',None)

    print "readPage - p_id: ", p_id

    if p_id != None:
        d = []
        page = models.PageEntity.objects.get(pk=p_id)
        configs = models.ConfigEntity.objects.filter(page=page)
        for c in configs:
            d.append(model_to_dict(c))
        response_data['data'] = d

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/api/login/')
def readPageList(request):
    print 'readPageList - uid: ', request.user.id
    response_data = {}
    response_data['status'] = 'ok'
    d = []
    pages = models.PageEntity.objects.filter(user=request.user)
    for p in pages:
        d.append(model_to_dict(p))
    response_data['data'] = d

    return HttpResponse(json.dumps(response_data), content_type="application/json")


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
    print '==', request.user.is_authenticated()

    return render_to_response(
        'configure/index.html',
        {},
        context_instance=RC(request, { 'user' : request.user}),
    )
    

def getdeals(request):
    ipstr = request.GET.get('ip',None)
    response_data = {}
    response_data['status'] = 'ok'
    result_str = ""
    if ipstr != None:
        result = _getDianpingDealsByIP(ipstr)
        if result != None:
            deals = []
            for deal in result['deals']:
                one_deal = {}
                one_deal['title'] = deal['title']
                one_deal['desc'] = deal['description']
                one_deal['image_url'] = deal['image_url']
                one_deal['list_price'] = deal['list_price']
                one_deal['current_price'] = deal['current_price']
                one_deal['purchase_count'] = deal['purchase_count']
                one_deal['city'] = deal['city']
                one_deal['cat'] = ','.join(deal['categories'])
                one_deal['deal_url'] = deal['deal_url']
                deals.append(one_deal)
            response_data['data'] = deals
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data['status'] = 'no'
            response_data['error'] = 'can not fetch data from backend!'
    else:
        response_data['status'] = 'no'
        response_data['error'] = 'No IP has been specified!'
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")

        
