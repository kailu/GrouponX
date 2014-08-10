#coding=utf-8

import hashlib
import urllib
import json
import utils

#请替换appkey和secret
appkey = "845109548"
secret = "5676c30202c144ec9dcc3b088a9ea488"
apiUrl = "http://api.dianping.com/v1/business/find_businesses"
apiUrl = "http://api.dianping.com/v1/deal/find_deals"

#示例参数
# paramSet = []
# paramSet.append(("format", "json"))
# paramSet.append(("city", "上海"))
# paramSet.append(("latitude", "31.21524"))
# paramSet.append(("longitude", "121.420033"))
# paramSet.append(("category", "美食"))
# paramSet.append(("region", "长宁区"))
# paramSet.append(("limit", "20"))
# paramSet.append(("radius", "2000"))
# #paramSet.append(("offset_type", "0"))
# #paramSet.append(("has_coupon", "1"))
# #paramSet.append(("has_deal", "1"))
# paramSet.append(("keyword", "泰国菜"))
# paramSet.append(("sort", "7"))

# #参数排序与拼接
# paramMap = {}
# for pair in paramSet:
# 	paramMap[pair[0]] = pair[1]

# codec = appkey
# for key in sorted(paramMap.iterkeys()):
# 	codec += key + paramMap[key]

# codec += secret

# #签名计算
# sign = (hashlib.sha1(codec).hexdigest()).upper()

# #拼接访问的URL
# url_trail = "appkey=" + appkey + "&sign=" + sign
# for pair in paramSet:
# 	url_trail += "&" + pair[0] + "=" + pair[1]

# requestUrl = apiUrl + "?" + url_trail

# #模拟请求
# response = urllib.urlopen(requestUrl)

# print response.read()

def _api(url,params):
    paramMap = {}
    for pair in params:
	paramMap[pair[0]] = pair[1]
    codec = appkey
    for key in sorted(paramMap.iterkeys()):
	codec += key + paramMap[key]
    codec += secret

    sign = (hashlib.sha1(codec).hexdigest()).upper()

    url_trail = "appkey=" + appkey + "&sign=" + sign
    for pair in params:
	url_trail += "&" + pair[0] + "=" + pair[1]

    requestUrl = url + "?" + url_trail
    response = urllib.urlopen(requestUrl)
    return json.loads(response.read())

#
# api document: http://developer.dianping.com/app/api/v1/metadata/get_categories_with_deals
def getCategories():
    params = []
   # params.append(('format','json'))

    url = 'http://api.dianping.com/v1/metadata/get_categories_with_deals'
    return _api(url,params)

def getGrouponByCity(city):
    params = []
    url = 'http://api.dianping.com/v1/deal/find_deals'
    params.append(('city',city))
    
    return _api(url,params)

def getGroupon(city,params):
    url = 'http://api.dianping.com/v1/deal/find_deals'
    params.append(('city',city))

    return _api(url,params)

def getAllDealCities():
    params = []
    url = "http://api.dianping.com/v1/metadata/get_cities_with_deals"
    
    return _api(url,params)


if __name__ == '__main__':
#    print getCategories()
#    gpons = getGrouponByCity('桂林')
#    print repr(gpons).decode('utf-8')

    # all_cities =  getAllDealCities()
    # for city in all_cities['cities']:
    #     print city.encode('utf8')

    gpons = getGrouponByCity('北京')
    gpons = utils.convert(gpons)
    for deal in gpons['deals']:
        print 'title:',deal['title']
        print 'description:',deal['description']
        print 'image_url:',deal['image_url']
        print 'list_price:',deal['list_price']
        print 'current_price:',deal['current_price']
        print 'purchase_count:',deal['purchase_count']
        print 'deal_url:',deal['deal_url']
        print 'city:',deal['city']
        print 'categories:',','.join(deal['categories'])
        print 
