import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.jeffersonbank.com'

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

def fetch_data():
    output_list = []
    url = "https://www.jeffersonbank.com/locations/json"
    request = requests.get(url)
    store_list = json.loads(request.text)['nodes']
    for store in store_list:
        store = store['node']
        geoinfo = json.loads(store['field_location_coordinates'])
        address = etree.HTML(store['Address'])
        hours = ""
        if store['Lobby Hours']:
            hours += "Lobby Hours: " + validate(etree.HTML(store['Lobby Hours']).xpath(".//text()"))
            if store['Motor Bank Hours']:
                hours += " Motor Bank Hours: " + validate(etree.HTML(store['Motor Bank Hours']).xpath(".//text()"))
        hours += " ATM: 24 hours / 7 Days a week"
        output = []
        output.append(base_url) # url
        output.append(validate(store['title'])) #location name
        output.append(validate(address.xpath('.//div[@class="street-block"]//text()'))) #address
        output.append(validate(address.xpath('.//span[@class="locality"]//text()'))) #city
        output.append(validate(address.xpath('.//span[@class="state"]//text()'))) #state
        output.append(validate(address.xpath('.//span[@class="postal-code"]//text()'))) #zipcode
        output.append('US') #country code
        output.append(validate(store['Nid'])) #store_number
        output.append(get_value(store['Phone'])) #phone
        output.append("Jefferson Bank") #location type
        output.append(geoinfo['coordinates'][0]) #latitude
        output.append(geoinfo['coordinates'][1]) #longitude
        output.append(hours) #opening hours
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
