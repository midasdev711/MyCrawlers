import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'https://googooexpresswash.com'

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
    url = "https://googooexpresswash.com/wp-admin/admin-ajax.php?action=store_search&max_results=1000&search_radius=50&autoload=1"
    headers = {
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    store_list = json.loads(response.text)
    for store in store_list:
        hours = get_value(etree.HTML(store['hours']).xpath(".//text()"))

        output = []
        output.append(base_url) # url
        output.append(validate(store['store'])) #location name
        output.append(validate(store['address'])) #address
        output.append(validate(store['city'])) #city
        output.append(validate(store['state'])) #state
        output.append(validate(store['zip'])) #zipcode
        output.append('US') #country code
        output.append(validate(store['id'])) #store_number
        output.append(validate(store['phone'])) #phone
        output.append("Goo-Goo Express Wash-Service") #location type
        output.append(validate(store['lat'])) #latitude
        output.append(validate(store['lng'])) #longitude
        output.append(validate(hours)) #opening hours
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
