# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext as RC

from django.shortcuts import render, render_to_response
from models import RegistrationForm
from django.contrib.auth.models import User

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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        new_user = User.objects.create_user(username, '', password)
        new_user.save()
        print "=== User: ", username, " password: ", password
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                print("User is valid, active and authenticated")
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

    


