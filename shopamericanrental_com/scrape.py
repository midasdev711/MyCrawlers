import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.shopamericanrental.com'

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
    url = "https://www.shopamericanrental.com/locations"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[contains(@class, "location-blocks")]//div[contains(@class, "block")]')
    for store in store_list:
        detail_url = validate(store.xpath("./a/@href"))
        detail_request = requests.get(base_url + detail_url)
        detail = etree.HTML(detail_request.text)
        zipcode = validate(detail.xpath('.//p/a/@href')[1].split('+').pop())
        city_state = validate(store.xpath('.//p[@class="address"]/span//text()'))
        hours = validate(detail.xpath('.//text()')).split('HOURS')[1].split('Contact the')[0]

        output = []
        output.append(base_url) # url
        output.append(validate(detail.xpath(".//h2//text()"))) #location name
        output.append(validate(store.xpath('.//p[@class="address"]/text()'))) #address
        output.append(city_state.split(', ')[0]) #city
        output.append(city_state.split(', ')[1]) #state
        output.append(zipcode) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append(validate(store.xpath('.//p[@class="phone"]//text()'))) #phone
        output.append("Shop online with American Rental to enjoy today's newest products and enhance your home.") #location type
        output.append("<MISSING>") #latitude
        output.append("<MISSING>") #longitude
        output.append(get_value(hours)) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
