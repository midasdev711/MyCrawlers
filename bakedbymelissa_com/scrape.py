import csv
import re
import pdb
import requests
from lxml import etree
import json

import usaddress

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options() 
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver', options=options)

base_url = 'https://www.bakedbymelissa.com'

def validate(items):
    rets = []
    for item in items:
        if not item:
            item = '<MISSING>'
        if item is '<MISSING>':
            pass
        else:
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
    url = "https://www.bakedbymelissa.com/locations/"
    driver.get(url)
    source = driver.page_source.encode('ascii', 'ignore').encode("utf-8")
    data = source.split('initial_locations:  ').pop().split('min_zoom')[0]
    store_data = json.loads(data[:-10])
    for store in store_data:
        output = []
        address = store.get('address').encode('utf-8')
        parsed_address = dict(usaddress.parse(address))
        parsed_address = {v: k for k, v in parsed_address.items()}
        street_address = (parsed_address.get("AddressNumber") or u'') + u' ' + (parsed_address.get("StreetNamePreDirectional") or u'') + u' ' + (parsed_address.get("StreetName") or u'') + u' ' + (parsed_address.get("StreetNamePostType") or u'')
        if street_address == '   ':
            tmp = address.split(' ')
            street_address = ' '.join(tmp[:-3])
        cityaddress = store.get('address_display').encode('utf-8').split('<br />')[1]
        cityaddress = dict(usaddress.parse(cityaddress))
        cityaddress = {v: k for k, v in cityaddress.items()}
        city = cityaddress.get("PlaceName")
        if parsed_address.get("StateName") == u'NY':
            city = 'New York'
        hourHTML = etree.HTML(store.get('notes').encode("utf-8"))
        hours = hourHTML.xpath('//p')
        store_hours = ""
        for hour in hours:
            store_hours += hour.xpath('.//strong/text()')[0] + ' ' + hour.xpath('./text()')[0] + ','
        store_hours = store_hours[:-1]
        output.append(base_url)
        output.append(store.get('title'))
        output.append(street_address)
        output.append(city)
        output.append(parsed_address.get("StateName"))
        output.append(parsed_address.get("ZipCode"))
        output.append(store.get('country'))
        output.append(store.get('location_id'))
        output.append('<MISSING>')
        output.append('Cake Store')
        output.append(store.get('latitude'))
        output.append(store.get('longitude'))
        output.append(store_hours)
        output_list.append(validate(output))
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
