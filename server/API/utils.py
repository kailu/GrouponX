

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
