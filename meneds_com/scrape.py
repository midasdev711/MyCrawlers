import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.meneds.com/'

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
    url = "https://www.meneds.com/wp-admin/admin-ajax.php?action=store_search&lat=36.80392&lng=-119.7909&max_results=100&search_radius=150&autoload=1"
    request = requests.get(url)
    store_list = json.loads(request.text)
    for store in store_list:
            
        output = []
        output.append(base_url) # url
        output.append(validate(store['store'])) #location name
        output.append(validate(store['address'] + store['address2'])) #address
        output.append(validate(store['city'])) #city
        output.append(validate(store['state'])) #state
        output.append(validate(store['zip'])) #zipcode
        output.append(validate(store['country'])) #country code
        output.append(validate(store['id'])) #store_number
        output.append(validate(store['phone'])) #phone
        output.append("Me-n-Ed's - Home of original California-style pizza, mouthwatering appetizers & sandwiches") #location type
        output.append(validate(store['lat'])) #latitude
        output.append(validate(store['lng'])) #longitude
        output.append(get_value(store['hours'])) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
