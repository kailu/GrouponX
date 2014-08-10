

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:

        return input


def convert_deals(data):
    deals = []
    for deal in data['deals']:
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
    return deals


def filter_deals(data,conf):
    filter_map = {}
    is_black_list = None

    if "" != conf.white_list:
        ll = conf.white_list.split(",")
        is_black_list = False
        for l in ll:
            filter_map[l] = True
        
    if "" != conf.black_list:
        ll = conf.black_list.split(",")
        is_black_list = True
        for l in ll:
            filter_map[l] = True

    deals = []
    for deal in data['deals']:
        is_a_valid_record = True
        if is_black_list == None:
            pass
        elif is_black_list == True:
            for c in deal['categories']:
                if filter_map.has_key(c):
                    is_a_valid_record = False
                    break
        else:
            is_a_valid_record = False
            for c in deal['categories']:
                if filter_map.has_key(c):
                    is_a_valid_record = True
                    break

        if not is_a_valid_record:
            continue
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
    return deals
    
        
