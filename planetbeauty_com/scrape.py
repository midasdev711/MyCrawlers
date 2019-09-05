import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.planetbeauty.com'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').encode("utf8").strip()

def get_value(item):
    if item == None or item == "0":
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
    url = "https://www.planetbeauty.com/storelocator/index/loadstore/"
    request = requests.post(url)
    store_list = json.loads(request.text)['storesjson']
    for store in store_list:

        output = []
        output.append(base_url) # url
        output.append(validate(store['store_name'])) #location name
        output.append(validate(store['address'])) #address
        output.append("<MISSING>") #city
        output.append("<MISSING>") #state
        output.append("<MISSING>") #zipcode
        output.append("US") #country code
        output.append(validate(store["storelocator_id"])) #store_number
        output.append(get_value(store["phone"])) #phone
        output.append("Planet Beauty Stores") #location type
        output.append(validate(store['latitude'])) #latitude
        output.append(validate(store['longitude'])) #longitude
        output.append("<MISSING>") #opening hours

        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
