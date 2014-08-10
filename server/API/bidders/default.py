# -*- coding: utf-8 -*-

from API import dianping
from API import baidu
from API import utils
import json


def defaultBidder(conf, params):
    """
    
    Arguments:
    - `conf`:
    """
    def bidder():
        #get ip from parms
        ip_str = params.get('ip',None)
        d = baidu.getAddressByIP(ip_str)
        try:
            d = json.loads(d)
            city = d['content']['address_detail']['city']

            if city.endswith(u"市"):
                city = city[:-1]
            city = city.encode('utf-8')
            #call dianping API
            gpons = dianping.getGrouponByCity(city)
            gpons = utils.filter_deals(gpons,conf)
            return gpons
        except Exception as ex:
            print ex
            return None

    return bidder
