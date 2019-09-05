import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'http://whitespot.ca'

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
    url = "http://whitespot.ca/locations.htm"
    session = requests.Session()
    request = session.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[@id="container-bottom"]//div[contains(@class, "views-row")]')
    for store in store_list:
        title = validate(store.xpath('.//div[@class="location-name"]/text()'))
        province = store.xpath('.//div[@class="location-city-province"]/text()')[0]
        city = province.split(',')[0]
        state = province.split(',')[1]
        zipcode = store.xpath('.//div[@class="location-postal-code"]/text()')[0]
        phone = store.xpath('.//div[@class="location-phone"]/text()')[0]
        hours = store.xpath('.//div[contains(@class, "views-field-field-hours-of-operation")]//text()')
        store_hours = get_value(hours).replace('Hours', '').replace('\n', '')
        
        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(validate(store.xpath('.//div[@class="location-street"]/text()'))) #address
        output.append(get_value(city)) #city
        output.append(get_value(state)) #state
        output.append(get_value(zipcode)) #zipcode
        output.append('CA') #country code
        output.append("<MISSING>") #store_number
        output.append(phone) #phone
        output.append("WhiteSpot-Restaurant") #location type
        output.append("<MISSING>") #latitude
        output.append("<MISSING>") #longitude
        output.append(store_hours) #opening hours        
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
