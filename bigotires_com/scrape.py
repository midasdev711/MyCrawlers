import csv
import re
import pdb
import requests
from lxml import etree
import json
import sgzip

base_url = 'https://www.bigotires.com'

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
    store_ids = []
    url = "https://www.bigotires.com/restApi/dp/v1/store/storesByAddress"
    with open('cities.json') as data_file:    
        city_list = json.load(data_file)
        for city in city_list:
            print(city['city'])
            data = {
                "address": city['city'],
                "distanceInMiles": "100"
            }

            request = requests.post(url, json=data)
            try:
                store_list = json.loads(request.text)['storesType']
            except:
                pdb.set_trace()
            if 'stores' not in store_list.keys():
                continue

            store_list = store_list['stores']
            for store in store_list:
                store_id = validate(store['storeId'])
                if store_id in store_ids:
                    continue
                store_ids.append(store_id)
                store_hours = store['workingHours']
                hours = ""
                for x in store_hours:
                    if validate(x['openingHour']) == 'Closed':
                        hours += validate(x['day'] + ': ' + x['openingHour'])
                    else:
                        hours += validate(x['day'] + ':' + x['openingHour'] + '-' + x['closingHour'] + ' ')
                storeClosedHours = store['storeClosedHours']
                for x in storeClosedHours:
                    hours += validate(x['date'] + ': ' + x['workingHours'] + ' ')

                output = []
                output.append(base_url) # url
                output.append(validate(store['address']['address1'])) #location name
                output.append(validate(store['address']['address1'])) #address
                output.append(validate(store['address']['city'])) #city
                output.append(validate(store['address']['state'])) #state
                output.append(validate(store['address']['zipcode'])) #zipcode
                output.append("US") #country code
                output.append(store_id) #store_number
                output.append(validate(store['phoneNumbers'][0])) #phone
                output.append("Big O Tires, your auto service experts") #location type
                output.append(store['mapCenter']['latitude']) #latitude
                output.append(store['mapCenter']['longitude']) #longitude
                output.append(get_value(hours)) #opening hours
                output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
