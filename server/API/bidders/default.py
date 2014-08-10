# -*- coding: utf-8 -*-

import API.dianping as dianping
import API.baidu as baidu
import API.utils as utils


def defautBidder(conf, params):
    """
    
    Arguments:
    - `conf`:
    """
    def bidder():
        #get ip from parms
        ip_str = parms.get('ip',None)
        d = baidu.getAddressByIP(ipstr)
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
