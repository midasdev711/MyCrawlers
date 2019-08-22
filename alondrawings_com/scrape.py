import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'http://lovealondras.com'

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

def write_output(data):
    with open('data.csv', mode='w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["locator_domain", "location_name", "street_address", "city", "state", "zip", "country_code", "store_number", "phone", "location_type", "latitude", "longitude", "hours_of_operation"])
        for row in data:
            writer.writerow(row)

def fetch_data():
    output_list = []
    url = "http://lovealondras.com/locations/"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "lovealondras.com",
        "Referer": "http://lovealondras.com/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    request = requests.get(url, headers=headers)
    response = etree.HTML(request.text)
    store_urls = response.xpath('//ul[@class="sydbar-ul-fld"]//a/@href')
    for store_url in store_urls:
        store_request = requests.get(store_url, headers=headers)
        store_response = etree.HTML(store_request.text)
        
        store = store_response.xpath('//div[contains(@class, "contnsect-fld-dflt")]')[0]
        street_address = get_value(store.xpath('.//p//text()')[0])
        address = get_value(store.xpath('.//p//text()')[1])
        index = 0
        try:
            city = address.split(',')[0]
            state = address.split(',')[1].split(' ')[1]
            zipcode = address.split(',')[1].split(' ')[2]
        except:
            address = get_value(store.xpath('.//p//text()')[2])
            city = address.split(',')[0]
            state = address.split(',')[1].split(' ')[1]
            zipcode = address.split(',')[1].split(' ')[2]
            index = 1

        geolocation = store.xpath('.//iframe/@src')[0]

        latitude =  geolocation.split('!2d-')[1].split('!3d')[0]
        longitude = geolocation.split('!2d-')[1].split('!3d')[1].split('!')[0]
        

        phone = get_value(store.xpath('.//p//text()')[2 + index])
        hours = get_value(store.xpath('.//p')[1].xpath('.//text()'))
        happyhours = get_value(store.xpath('.//p')[2].xpath('.//text()')[0])
        lunchtime = get_value(store.xpath('.//p')[3].xpath('.//text()')[0])
        store_hours = validate("Hours: " + hours + " Happy hour: " + happyhours + " Lunch time special: " + lunchtime)
        output = []
        output.append(base_url) # url
        output.append(validate(store.xpath('.//h3/text()')[0])) #location name
        output.append(street_address) #address
        output.append(get_value(city)) #city
        output.append(get_value(state)) #state
        output.append(get_value(zipcode)) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append(phone) #phone
        output.append("ALONDRAS'S - Craft American Eatery") #location type
        output.append(latitude) #latitude
        output.append(longitude) #longitude
        output.append(store_hours.replace('\n', '')) #opening hours       
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
