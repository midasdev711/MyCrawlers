import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'http://www.tcby.com'

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
    url = "https://www.tcby.com/find-a-store/"
    request = requests.get(url)
    response = etree.HTML(request.text.encode("utf-8"))
    state_list = eliminate_space(response.xpath('//select[@class="usa-select"]//option//text()'))[1:]
    for state in state_list:
        store_list = json.loads(requests.get("https://www.tcby.com/api/geo/" + state).text)
        for store in store_list:
            output = []
            output.append(base_url) # url
            output.append(validate(store['name'])) #location name
            output.append(validate(store['address'])) #address
            output.append(validate(store['city'])) #city
            output.append(state) #state
            output.append(get_value(store['zip'])) #zipcode
            output.append("US") #country code
            output.append(validate(store['id'])) #store_number
            output.append(validate(store['phone'])) #phone
            output.append("TCBY - The Country's Best Yogurt Stores") #location type
            output.append(validate(store['latitude'])) #latitude
            output.append(validate(store['longitude'])) #longitude
            output.append(get_value(store['hours'])) #opening hours
            output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
