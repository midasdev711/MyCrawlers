import csv
import re
import pdb
import requests
from lxml import etree
import json


base_url = 'http://www.eatsnarfs.com/'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.replace(u'\u2013', '-').encode('ascii', 'ignore').encode("utf8").strip()

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
    url = "http://www.eatsnarfs.com/services/location/get_all_stores.php"
    request = requests.get(url)
    store_list = json.loads(request.text)['places']['positions']
    for store in store_list:
        if store['comingSoon'] == True or store['hours'] == 'Closed':
            continue

        detail_url = store['url']
        detail_request = requests.get(base_url + detail_url)
        detail = etree.HTML(detail_request.text)

        phone = get_value(detail.xpath("//div[@class='contact']//text()"))
        hours = get_value(eliminate_space(detail.xpath("//table[@class='hours']//text()")))
        output = []
        output.append(base_url) # url
        output.append(validate(store['name'])) #location name
        output.append(validate(store['street'])) #address
        output.append(validate(store['city'])) #city
        output.append(validate(store['state'])) #state
        output.append(validate(store['zip'])) #zipcode
        output.append('US') #country code
        output.append(str(store['id'])) #store_number
        output.append(phone) #phone
        output.append("Snarf's Sandwiches - Restaurant") #location type
        output.append(store['location']['lat']) #latitude
        output.append(store['location']['lng']) #longitude
        output.append(hours) #opening hours        
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
