import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://soulmans.com'

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
    url = "https://soulmans.com/wp-admin/admin-ajax.php?action=store_search&lat=32.66042&lng=-96.76011&max_results=50&search_radius=250"
    headers = {
        "cookie": "__cfduid=da6b0160b3e5e854f5c1f3de4c5353f341568070666; _ga=GA1.2.1851317785.1568070673; _gid=GA1.2.2129001813.1568070673; __utma=232391709.1851317785.1568070673.1568070674.1568070674.1; __utmc=232391709; __utmz=232391709.1568070674.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; _fbp=fb.1.1568070674433.815462564; PHPSESSID=54e440c84c139694a6d93c512bb7585b; __utmb=232391709.3.10.1568070674",
        "referer": "https://soulmans.com/locations/",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    request = requests.get(url, headers=headers)
    store_list = json.loads(request.text)
    for store in store_list:
            
        output = []
        output.append(base_url) # url
        output.append(validate(store['store']).replace('&#8211;', '-').replace('&#8217;', "'").split('-')[0]) #location name
        output.append(validate(store['address'] + store['address2'])) #address
        output.append(validate(store['city'])) #city
        output.append(validate(store['state'])) #state
        output.append(validate(store['zip'])) #zipcode
        output.append(validate(store['country'])) #country code
        output.append(validate(store['id'])) #store_number
        output.append(validate(store['phone'])) #phone
        output.append("Soulman's Bar-B-Que") #location type
        output.append(validate(store['lat'])) #latitude
        output.append(validate(store['lng'])) #longitude
        output.append(get_value(etree.HTML(store['hours']).xpath('.//text()'))) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
