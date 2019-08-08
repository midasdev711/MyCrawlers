import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.birkenstock.com'

def validate(items):
    rets = []
    for item in items:
        if item is '<MISSING>':
            continue
        if type(item) != str:
            item = str(item)
        item = item.encode('utf-8').strip()
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
    url = "https://www.birkenstock.com/on/demandware.store/Sites-US-Site/en_US/Stores-GetStoresJson?latitude=40.724351&longitude=-74.001120&latituderef=40.724351&longituderef=-74.001120&storeid=&distance=19&distanceunit=mi&searchText=&countryCode=US&storeLocatorType=regular"
    session = requests.Session()
    request = session.get(url)
    store_list = json.loads(request.text)['stores']
    store_keys = list(store_list.keys())
    for x in store_keys:
        store = store_list[x]
        output = []
        storeHours = "Mon - Sat : 10.a.m - 8.p.m, Sun : 11.a.m - 7.p.m"

        if store.get('storeHoursHTML') == "":
            storeHours = "<MISSING>"
        if store.get('phone'):
            phone = store.get('phoneAreaCode') + ' ' + store.get('phone')
        else:
            phone = '<MISSING>'
            
        output.append(base_url)
        output.append(store.get('name'))
        output.append(store.get('address1'))
        output.append(store.get('city'))
        output.append(store.get('state'))
        output.append(store.get('postalCode'))
        output.append(store.get('countryCode'))
        output.append(store.get('id'))
        output.append(phone)
        output.append(store.get('storeLocatorType'))
        output.append(store.get('latitude'))
        output.append(store.get('longitude'))
        output.append(storeHours)
        output_list.append(validate(output))
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
