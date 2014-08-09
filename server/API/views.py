# -*- coding: utf-8 -*-
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


def login_(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print("User is valid, active and authenticated")
                print "domain: ", user.site.domain
                return HttpResponseRedirect('../page/')
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
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

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        domain = request.POST['domain']
        print "=== User: ", username, " password: ", password, 'domain: ', domain

        new_user = User.objects.create_user(username, '', password)

        hasher = hashlib.md5()
        hasher.update(username + domain)
        h = hasher.hexdigest()
        site = Site(user=new_user, hash=h, domain=domain)
        site.save()
        new_user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print("User is valid, active and authenticated")
                print "domain: ", user.site.domain
                return HttpResponseRedirect('../page/')
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
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
    

