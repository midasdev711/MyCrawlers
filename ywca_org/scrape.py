import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'https://www.ywca.org/'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').encode("utf8").strip().replace('\n', '').replace('\t\t', '')

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
    url = "https://secure2.convio.net/ywca/map/locations.csv"
    response = requests.get(url)
    store_list = []
    for item in response.text.split('\r\n'):
        store_list.append(item.split(','))
    store_list = store_list[1:]
    store_list.pop()
    for store in store_list:
        title = validate(store[0])
        param = 0;
        if len(store) == 8:
            street_address = validate(store[1])
            city = validate(store[2][1:])
            state = validate(store[3].split(' ')[1])
            zipcode = validate(store[3].split(' ')[2][:-1])
            phone = validate(store[4])
            latitude = validate(store[5])
            longitude = validate(store[6])
        elif len(store) == 9:
            street_address = store[1] + ',' + store[2]
            param = 1
        else:
            street_address = store[1] + ',' + store[2] + ',' + store[3]
            param = 2
        city = validate(store[2 + param][1:])
        state = validate(store[3 + param].split(' ')[1])
        zipcode = validate(store[3 + param].split(' ')[2][:-1])
        phone = validate(store[4 + param]).replace('|', '')
        latitude = validate(store[5 + param])
        longitude = validate(store[6 + param])

        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(street_address) #address
        output.append(city) #city
        output.append(state) #state
        output.append(zipcode) #zipcode
        output.append('US') #country code
        output.append('<MISSING>') #store_number
        output.append(phone) #phone
        output.append("YWCA") #location type
        output.append(latitude) #latitude
        output.append(longitude) #longitude
        output.append('<MISSING>') #opening hours
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
