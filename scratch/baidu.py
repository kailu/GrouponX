# -*- coding: utf-8 -*-

import urllib
import hashlib
import json

ak = "kCQunAYX7Tuc68wfRnHnhN78"
#ak = "yourak"
sk = "EuAwdTyqjQP3MVD6gAQtu7GiCWe52N1o"
#sk = "yoursk"

def sign(url,params):

    paramStr = ""
#    params['output'] = 'json'
    paramList = []
    for key in sorted(params.iterkeys()):
        newkey = key
        newval = params[key]
     
        paramList.append((newkey,newval))

    paramList.append(('ak',ak))
    paramStr = urllib.urlencode(paramList)

    apiUrl = url
#    if not apiUrl.endswith("/"):
#        apiUrl += "/"
    apiUrl += "?" + paramStr + sk
 
    
    m = hashlib.md5()

    apiUrl = urllib.quote_plus(apiUrl)
    m.update(apiUrl)

    return m.hexdigest()


def api(url,path,params):
    sign_str = sign(path,params)
    paramStr = ""
#    params['output'] = 'json'
    paramList = []
    for key in sorted(params.iterkeys()):
        newkey = key
        newval = params[key]
     
        paramList.append((newkey,newval))

    paramList.append(('ak',ak))
    paramList.append(('sn',sign_str))
    paramStr = urllib.urlencode(paramList)    

    apiUrl = url + "?" + paramStr
    print apiUrl
    response = urllib.urlopen(apiUrl)
    return response.read()

def getAddressByIP(ipstr):
    url = "http://api.map.baidu.com/location/ip"
    path = "/location/ip"
    params = {}
#    params['coor'] = 'bd09ll'
    params['ip'] = ipstr

    return api(url,path,params)

if __name__ == '__main__':
#    print json.loads(getAddressByIP('10.73.222.175'))['message'].encode('utf-8')
    d = getAddressByIP('202.193.16.3')
    print d
    d = json.loads(d)
    print d['content']['address_detail']['city'].encode('utf-8')
    
    
    

    
        
