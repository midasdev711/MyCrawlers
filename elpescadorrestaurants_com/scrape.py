import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'https://www.elpescadorrestaurants.com'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.replace(u'\u2013', '-').encode('ascii', 'ignore').encode("utf8").strip()

def get_value(item):
    item = validate(item)
    if item == '':
        item = '<MISSING>'    
    return item

def eliminate_space(items):
    rets = []
    for item in items:
        item = validate(item)
        if item != '':
            rets.append(item)
    return rets

def parse_address(address):
    address = usaddress.parse(address)
    street = ''
    city = ''
    state = ''
    zipcode = ''
    for addr in address:
        if addr[1] == 'PlaceName':
            city += addr[0].replace(',', '') + ' '
        elif addr[1] == 'ZipCode':
            zipcode = addr[0]
        elif addr[1] == 'StateName':
            state = addr[0]
        else:
            street += addr[0].replace(',', '') + ' '

    return { 
            'street': get_value(street), 
            'city' : get_value(city), 
            'state' : get_value(state), 
            'zipcode' : get_value(zipcode)
            }

def write_output(data):
    with open('data.csv', mode='w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["locator_domain", "location_name", "street_address", "city", "state", "zip", "country_code", "store_number", "phone", "location_type", "latitude", "longitude", "hours_of_operation"])
        for row in data:
            writer.writerow(row)

def fetch_data():
    output_list = []
    url = "https://www.powr.io/plugins/map/wix_view.json?cacheKiller=1565888152975&compId=comp-iyxnhaf3&deviceType=desktop&height=733&instance=ruDOCgXTqtozvxaejnoTEnsKByMe6CQuwx8vjQu_YBA.eyJpbnN0YW5jZUlkIjoiN2M0Y2M2MDAtYThlYS00N2IzLTkxYzItOWFhMzI3MmE4NTgwIiwiYXBwRGVmSWQiOiIxMzQwYzVlZC1hYWM1LTIzZWYtNjkzYy1lZDIyMTY1Y2ZkODQiLCJzaWduRGF0ZSI6IjIwMTktMDgtMTZUMTI6MTc6MzQuMzczWiIsInVpZCI6bnVsbCwiaXBBbmRQb3J0IjoiMTA3LjE4MS4xNzcuMTMvNjAxNzYiLCJ2ZW5kb3JQcm9kdWN0SWQiOiJwcmVtaXVtIiwiZGVtb01vZGUiOmZhbHNlLCJhaWQiOiIwZWNiOTNkZS04MzkxLTQyMTgtYWRkOS1hNDVhZTA2ODVkMGUiLCJzaXRlT3duZXJJZCI6IjkwODczMDkwLWNiNzEtNDA0ZC05NDhhLTEwZGVjOTc2MjNkNSJ9&locale=en&pageId=fewkh&siteRevision=46&viewMode=site&width=100%25"
    request = requests.get(url)
    store_list = json.loads(request.text)['content']['locations']
    for store in store_list:
        address = store['address']
        address = parse_address(address)
        
        detail = etree.HTML(store['description'])

        output = []
        output.append(base_url) # url
        output.append(get_value(etree.HTML(store['name']).xpath(".//text()"))) #location name
        output.append(validate(address['street'])) #address
        output.append(validate(address['city'])) #city
        output.append(validate(address['state'])) #state
        output.append(validate(address['zipcode'][:-1])) #zipcode
        output.append("US") #country code
        output.append("<MISSING>") #store_number
        output.append(validate(detail.xpath('.//p//text()')[2])) #phone
        output.append("El Pescador restaurant") #location type
        output.append(store['lat']) #latitude
        output.append(store['lng']) #longitude
        output.append("<MISSING>") #opening hours        
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
