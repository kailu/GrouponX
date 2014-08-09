from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return HttpResponse("hello, world!")


@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
def createPageID(request):
    """
    
    Arguments:
    - `request`:
    """
    pass




