import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://eatbychloe.com'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').encode("utf8").strip().replace('\n', '').replace('\t', '')

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
    url = "https://eatbychloe.com/locations/"
    session = requests.Session()
    request = session.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[@id="locations-sidebar"]')[0].xpath('.//div[@class="location-item"]')
    for store in store_list:
        data_address = store.xpath('./@data-address')[0].split(', ')
        street_address = data_address[1]
        title = get_value(store.xpath('.//div[@class="location-wrap"]//text()'))
        if 'COMING SOON!' in title:
            continue
        
        output = []
        output.append(base_url) # url
        output.append(title) #location name
        
        info = eliminate_space(store.xpath('./p//text()'))
        if len(info) > 3:
            address = info[1:]
        else:
            address = info
        output.append(validate(address[0])) #address
        address = address[1].split(',')
        output.append(address[0]) #city
        if len(address) == 3:
            output.append(address[1].strip().split(' ')[0]) #state
            output.append(address[2].strip().split(' ')[0]) #zipcode
        elif len(address) == 2:
            output.append(address[1].strip().split(' ')[0]) #state
            output.append(address[1].strip().split(' ')[1]) #zipcode

        output.append(store.xpath('./@data-address')[0].split(', ').pop()) #country code
        output.append("<MISSING>") #store_number
        if len(info) > 2:
            output.append(validate(info.pop())) #phone
        else:
            output.append("<MISSING>") #phone
        output.append("Classic Taste, Plant-Based | Vegan Restaurant") #location type
        output.append(store.xpath('./@data-latlng')[0].split(',')[0]) #latitude
        output.append(store.xpath('./@data-latlng')[0].split(',')[1]) #longitude
        output.append(get_value(store.xpath('.//div[@class="hours-item"]//text()'))) #opening hours
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
