import csv
import re
import pdb
import requests
from lxml import etree
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options() 
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver', options=options)

base_url = "https://www.abcstores.com/"

def validate(items):
    rets = []
    for item in items:
        if item is '<MISSING>':
            continue
        item = item.encode('utf-8').replace('\xef\xbb\xbf', '').strip()
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
    url = "https://www.abcstores.com/storelocator/"
    driver.get(url)
    source = driver.page_source.encode('ascii', 'ignore').encode("utf8")
    data = source.split('AmLocation.Amastyload(').pop().split(');')[0]
    store_data = json.loads(data).get('items')
    for store in store_data:
        output = []
        output.append(base_url)
        output.append(store.get('name'))
        output.append(store.get('address'))
        output.append(store.get('city'))
        output.append(store.get('state'))
        output.append(store.get('zip'))
        output.append(store.get('country'))
        output.append(store.get('id'))
        output.append(store.get('phone'))
        output.append('ABC Stores - The Store with Aloha')
        output.append(store.get('lat'))
        output.append(store.get('lng'))
        output.append(store.get('description'))
        output_list.append(validate(output))
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
