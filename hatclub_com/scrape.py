import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.hatclub.com'

def validate(items):
    rets = []
    for item in items:
        
        if item is '<MISSING>':
            continue
        if type(item) is int:
            pass
        else:
            item = item.encode('ascii','ignore').encode('utf-8').replace(u'\xa0', '').strip()

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
    url = "https://storelocator.w3apps.co/get_stores2.aspx?shop=hat-club&all=1"
    headers={
        "Accept": "*/*",
        'Referer': 'https://storelocator.w3apps.co/map.aspx?shop=hat-club&container=true',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
        }
    request = requests.post(url, headers=headers)
    store_list = json.loads(request.text)['location']
    for store in store_list:
        output = []
        output.append(base_url)
        output.append(store.get('name'))
        output.append(store.get('address'))
        output.append(store.get('city'))
        output.append(store.get('state'))
        output.append(store.get('zip'))
        output.append('US')
        output.append(store.get('id'))
        output.append(store.get('phone'))
        output.append('HAT CLUB')
        output.append(store.get('lat'))
        output.append(store.get('long'))
        output.append('<MISSING>')
        output_list.append(validate(output))
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
