import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'https://midwoodsmokehouse.com'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').encode("utf8").strip()

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

def write_output(data):
    with open('data.csv', mode='w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["locator_domain", "location_name", "street_address", "city", "state", "zip", "country_code", "store_number", "phone", "location_type", "latitude", "longitude", "hours_of_operation"])
        for row in data:
            writer.writerow(row)

def fetch_data():
    output_list = []
    url = "https://midwoodsmokehouse.com/locations/"
    session = requests.Session()
    request = session.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[contains(@class, "locations-listing")]//div[@class="inside"]')
    for store in store_list:
        title = get_value(store.xpath('.//div[@class="address-info"]//h3[@class="name"]/text()'))
        street_address = get_value(store.xpath('.//div[@class="address-info"]//div[contains(@class, "add1")]//text()'))
        city = get_value(store.xpath('.//div[@class="address-info"]//div[contains(@class, "add2")]//text()')).split(',')[0]
        state = get_value(store.xpath('.//div[@class="address-info"]//div[contains(@class, "add2")]//text()')).split(',')[1]
        phone = get_value(store.xpath('.//div[@class="address-info"]//div[@class="phone"]//text()'))
        hours = get_value(store.xpath('.//div[@class="hours"]//text()'))
        store_hours = get_value(hours).replace('Hours', '').replace('\n', '')
        
        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(street_address) #address
        output.append(city) #city
        output.append(state) #state
        output.append('<MISSING>') #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append(phone) #phone
        output.append("Midwood Smokehouse - BBQ Restaurant & Bar") #location type
        output.append("<MISSING>") #latitude
        output.append("<MISSING>") #longitude
        output.append(store_hours) #opening hours        
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
