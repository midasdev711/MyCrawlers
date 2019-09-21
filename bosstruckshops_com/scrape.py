import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://bosstruckshops.com'

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
    url = "https://bosstruckshops.com/locations-by-state/"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_url_list = response.xpath('//article//li[contains(@class, "menu-item")]//a/@href')
        
    for store_url in store_url_list:
        store_request = requests.get(store_url)
        store = etree.HTML(store_request.text)

        title = validate(store.xpath(".//h1//text()")[0])[:-1]
        info = store.xpath('.//div[contains(@class, "et_pb_section_1")]//div[@class="et_pb_text_inner"]')
        phone = eliminate_space(info[0].xpath('.//text()')).pop()
        hours = eliminate_space(info[0].xpath('.//text()'))[2]
        if title == 'Myerstown, Pennsylvani':
            hours = eliminate_space(info[0].xpath('.//text()'))[1]
        city_state_zip = eliminate_space(info[2].xpath('.//text()'))[1].split(', ')
        city = city_state_zip.pop(0)
        if len(city_state_zip) == 1:
            state = city_state_zip[0].split(' ')[0]
            zipcode = city_state_zip[0].split(' ')[1]
        else:
            state = city_state_zip[0]
            zipcode = city_state_zip[1]
        geoinfo = validate(store.xpath('.//div[contains(@class, "et_pb_section_1")]//a/@href').pop())
        latitude = geoinfo.split('@')[1].split(',')[0]
        longitude = geoinfo.split('@')[1].split(',')[1]

        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(eliminate_space(info[2].xpath('.//text()'))[0]) #address
        output.append(city) #city
        output.append(state) #state
        output.append(zipcode) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append(phone) #phone
        output.append("Boss Shop | Semi-Trailer Truck Service and Preventative Maintenance") #location type
        output.append(latitude) #latitude
        output.append(longitude) #longitude
        output.append(hours.replace('Open:', '')) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
