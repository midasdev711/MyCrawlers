import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://urban-planet.com'

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
    url = "https://urban-planet.com/apps/api/v1/stores?&_=1567285562921"
    request = requests.get(url)
    store_list = json.loads(request.text)['stores']
    for store in store_list:
        country_code = validate(store['address']['country'])
        if country_code != 'United States' and country_code != 'Canada':
            continue
        opening_hours = store['open_hours']
        address = store['address']['line1']
        if store['address']['line2'] != None:
            address += ' ' + store['address']['line2']

        state = store['address']['state_code']
        if state == None:
            state = store['address']['state']

        hours = ""

        for opening_hour in opening_hours:
            hours += opening_hour['day'][:3] + ': ' + opening_hour['open_time'] + '-' + opening_hour['close_time'] + ' '

        output = []
        output.append(base_url) # url
        output.append(validate(store['address']['name'])) #location name
        output.append(validate(address)) #address
        output.append(validate(store['address']['city'])) #city
        output.append(validate(state)) #state
        output.append(validate(store['address']['zip'])) #zipcode
        output.append(country_code) #country code
        output.append(validate(store["store_code"])) #store_number
        output.append(get_value(store["phone"])) #phone
        output.append("Shop Urban Planet for the latest in womens, mens, girls and boys fashions at affordable prices") #location type
        output.append(store['address']['latitude']) #latitude
        output.append(store['address']['longitude']) #longitude
        output.append(hours) #opening hours

        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
