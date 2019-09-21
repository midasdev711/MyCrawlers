import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.dogtopia.com'

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
    url = "https://www.dogtopia.com/wp-json/store-locator/v1/locations.json"
    request = requests.get(url)
    store_list = json.loads(request.text)
    for store in store_list:
        if store['opening_soon']:
            continue
        location_address_info = store['store_info']["location_address_info"][0]
        location_hours_info = store['store_info']['location_hours_info'][0]
        hours = {"monday": {}, "tuesday": {}, "wednesday": {}, "thursday": {}, "friday": {}, "saturday": {}, "sunday": {}}
        extra = ""
        for idx, item in location_hours_info.items():
            label = validate(idx).split('_')
            if label[0] == "coming":
                continue
            hour_data = {label[1]: validate(item)}
            if label[0] not in list(hours.keys()):
                extra += validate(item)
                continue
            tmp = dict(hours[label[0]])
            tmp.update(hour_data)
            hours[label[0]] = tmp
        store_hours = ""
        count = 0
        for idx, item in hours.items():
            if len(item.keys()) < 2:
                store_hours += idx + ' Closed '
            else:
                store_hours += idx + item['open'] + '-' + item['close'] + ' '
                count += 1
        if count == 0:
            continue
        store_hours += extra
            
        output = []
        output.append(base_url) # url
        output.append(validate(store['title']['raw'])) #location name
        output.append(validate(location_address_info['location_street_address'])) #address
        output.append(validate(location_address_info['location_city'])) #city
        output.append(validate(location_address_info['location_state_prov'])) #state
        output.append(validate(location_address_info['location_zip_postal'])) #zipcode
        output.append(validate(location_address_info['location_country'])) #country code
        output.append(get_value(location_address_info.get('location_id'))) #store_number
        output.append(validate(location_address_info['location_phone'])) #phone
        output.append("Dogtopia - The leading provider of dog daycare in North America") #location type
        output.append(validate(location_address_info['location_coordinates']['latitude'])) #latitude
        output.append(validate(location_address_info['location_coordinates']['longitude'])) #longitude
        output.append(get_value(store_hours)) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
