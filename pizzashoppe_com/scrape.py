import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress

base_url = 'http://pizzashoppe.com/'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').encode("utf8").strip()

def get_value(item):
    if item == None :
        item = '<MISSING>'
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

def write_output(data):
    with open('data.csv', mode='w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["locator_domain", "location_name", "street_address", "city", "state", "zip", "country_code", "store_number", "phone", "location_type", "latitude", "longitude", "hours_of_operation"])
        for row in data:
            writer.writerow(row)

def parse_address(address):
    address = usaddress.parse(address)
    street = ''
    city = ''
    state = ''
    zipcode = ''
    country = ''
    for addr in address:
        if addr[1] == 'PlaceName':
            city += addr[0].replace(',', '') + ' '
        elif addr[1] == 'ZipCode':
            zipcode = addr[0].replace(',', '')
        elif addr[1] == 'StateName':
            state = addr[0].replace(',', '')
        elif addr[1] == 'CountryName':
            country = addr[0].replace(',', '')
        else:
            street += addr[0].replace(',', '') + ' '

    return { 
            'street': get_value(street), 
            'city' : get_value(city), 
            'state' : get_value(state), 
            'zipcode' : get_value(zipcode),
            'country': get_value(country)
            }

def fetch_data():
    output_list = []
    url = "http://pizzashoppe.com/locations/"
    request = requests.get(url)
    response = request.text.split(' var locations = ')[1].split('function initMap')[0].replace('//', '').replace('lat:', '"lat":').replace('lng:', '"lng":').replace('\n', '').replace('\x03', '')
    store_list = json.loads(response)
    for store in store_list:
        if 'Martin City' in validate(store['name']):
            continue
        address = parse_address(store['full-address'])
            
        output = []
        output.append(base_url) # url
        output.append(validate(store['name'])) #location name
        output.append(validate(store['address'])) #address
        output.append(validate(address['city'])) #city
        output.append(validate(address['state'])) #state
        output.append(validate(address['zipcode'])) #zipcode
        output.append(validate('US')) #country code
        output.append(validate(store['place-id'])) #store_number
        output.append(validate(store['phone'])) #phone
        output.append("Kansas City's Original Neighborhood Pizza Place") #location type
        output.append(store['l-l']['lat']) #latitude
        output.append(store['l-l']['lng']) #longitude
        output.append('<MISSING>') #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
