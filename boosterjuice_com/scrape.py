import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.boosterjuice.com'

def validate(items):
    rets = []
    for item in items:
        
        if item is '<MISSING>':
            continue

        item = item.encode('ascii','ignore').encode('utf-8').replace(u'\xba', '').strip()
        if item != '':
            rets.append(item)
    return rets

def write_output(data):
    with open('data.csv', mode='w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["locator_domain", "location_name", "street_address", "city", "state", "zip", "country_code", "store_number", "phone", "location_type", "latitude", "longitude", "hours_of_operation"])
        for row in data:
            writer.writerow(row)
    return

def fetch_data():
    output_list = []
    url = "https://www.boosterjuice.com/WebServices/Booster.asmx/StoreLocations"
    session = requests.Session()
    request = session.get(url)
    store_list = json.loads(request.text)
    for store in store_list:
        output = []
        hours = store.get('hours')
        store_hours = ""
        if len(hours) > 0:
            for x in hours:
                store_hours += (x.get('day') or u' ') + u' ' + (x.get('open') or u' ') + u' ' + (x.get('close') or u' ') + u','
        if store.get('postalCode').encode('utf-8')[:1] >= 'A' and store.get('postalCode').encode('utf-8')[:1] <= 'Z':
            country_code = 'CA'
        else:
            country_code = 'US'
        output.append(base_url)
        output.append(store.get('name'))
        output.append(store.get('address'))
        output.append(store.get('city'))
        output.append(store.get('province'))
        output.append(store.get('postalCode'))
        output.append(country_code)
        output.append(str(store.get('number')))
        output.append(store.get('phoneNumber'))
        output.append('Booster Juice')
        output.append(str(store.get('latitude')))
        output.append(str(store.get('longitude')))
        output.append(store_hours)
        output_list.append(validate(output))
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
