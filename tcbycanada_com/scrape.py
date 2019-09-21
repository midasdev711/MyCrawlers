import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'http://www.tcbycanada.com'

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
    url = "http://www.tcbycanada.com/wp-content/plugins/superstorefinder-wp/ssf-wp-xml.php?wpml_lang=fr&t=1567446471949"
    request = requests.get(url)
    response = etree.HTML(request.text.encode("utf-8"))
    store_list = response.xpath('//locator//store//item')
    for store in store_list:
        address = validate(store.xpath('.//address//text()'))
        address = address.split('  ')
        if len(address) == 1:
            address = get_value(address).split(',')
        if len(address) == 1:
            state = "<MISSING>"
        else:
            state = validate(address.pop())
        if 'QC' in state:
            zipcode = state[3:]
            state = state[:3]
        else:
            zipcode = '<MISSING>'
        street = validate(address)
        if '1503' in street or '6142' in street or '4211' in street:
            street = street.split(' ')
            city = street.pop()[:-1]
            street = validate(street)
        else:
            city = "<MISSING>"
        output = []
        output.append(base_url) # url
        output.append(validate(store.xpath('.//location//text()'))) #location name
        output.append(street) #address
        output.append(city) #city
        output.append(state) #state
        output.append(zipcode) #zipcode
        output.append("CA") #country code
        output.append(store.xpath('.//text()').pop()) #store_number
        output.append(get_value(store.xpath('.//telephone//text()'))) #phone
        output.append("TCBY - The Country's Best Yogurt Stores") #location type
        output.append(validate(store.xpath('.//latitude//text()'))) #latitude
        output.append(validate(store.xpath('.//longitude//text()'))) #longitude
        output.append(get_value(store.xpath('.//operatingHours//text()'))) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
