import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.indochino.com'

def validate(item):
    if type(item) == list:
        item = ' '.join(item)
    while True:
        if item[-1:] == ' ':
            item = item[:-1]
        else:
            break
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
    url = "https://www.indochino.com/showrooms"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[contains(@class, "showroomLocations__LOC")]')
    for store in store_list:
        data_id = validate(store.xpath('./@data-id'))
        if data_id == "29463" or data_id == "29934" or data_id == "29560" or data_id == "28474":
            continue
        country = validate(store.xpath('./@class'))
        if 'cnt-US' in country:
            country = 'US'
        else:
            country = 'CA'
        city_state = get_value(store.xpath('.//div[@class="city"]//text()'))
        output = []
        output.append(base_url) # url
        output.append(validate(store.xpath('./@name'))) #location name
        output.append(get_value(store.xpath('.//div[@class="street"]//text()'))) #address
        output.append(city_state[:-4]) #city
        output.append(city_state[-2:]) #state
        output.append("<MISSING>") #zipcode
        output.append(country) #country code
        output.append(data_id) #store_number
        output.append(get_value(store.xpath('.//div[@class="tel"]//text()'))) #phone
        output.append("INDOCHINO | Men's Custom Suits") #location type
        output.append(validate(store.xpath('./@data-latitude'))) #latitude
        output.append(validate(store.xpath('./@data-longitude'))) #longitude
        output.append(get_value(eliminate_space(store.xpath('.//div[@class="showroomLocations__hours"]//text()'))[1:]).replace('\n', '')) #opening hours
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
