import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.jamiesonvitamins.com'

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
    url = "https://stores.boldapps.net/front-end/get_surrounding_stores.php?shop=jamieson-5.myshopify.com&latitude=43.65521373252041&longitude=-79.38720649999999&max_distance=0&limit=500&calc_distance=0"
    request = requests.get(url)
    store_list = json.loads(request.text)['stores']
    for store in store_list:
        output = []
        output.append(base_url) # url
        output.append(validate(store['name'])) #location name
        output.append(validate(store['address'] + store['address2'])) #address
        output.append(validate(store['city'])) #city
        output.append(validate(store['prov_state'])) #state
        output.append(validate(store['postal_zip'])) #zipcode
        output.append(validate(store['country'])) #country code
        output.append(validate(store['store_id'])) #store_number
        output.append(get_value(store['phone'])) #phone
        output.append("Jamieson Vitamins - Bottle Service and personalized subscription service") #location type
        output.append(validate(store['lat'])) #latitude
        output.append(validate(store['lng'])) #longitude
        output.append(get_value(store['hours'])) #opening hours
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
