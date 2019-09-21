import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.harrywinston.com'

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
    url = "https://www.harrywinston.com/en/salon-locations/locations?region=287&country=all&city=all"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//li[contains(@class, "search-result-item")]')
    for store in store_list:
        name = store.xpath(".//h2[@class='result-item-name']")[0]
        geoinfo = get_value(name.xpath("./@data-localisation"))
        original_address = get_value(store.xpath('.//div[@class="result-item-address"]//text()'))
        address = original_address.split(',')
        country_code = address.pop()
        state_zip = eliminate_space(address.pop().split(' '))
        state = validate(state_zip.pop(0))
        zipcode = get_value(state_zip)
        hours = eliminate_space(store.xpath('.//div[contains(@class, "schedule-container")]//text()'))
        output = []
        output.append(base_url) # url
        output.append(get_value(name.xpath('.//text()'))) #location name
        output.append(get_value(eliminate_space(original_address.split(','))[:-3])) #address
        output.append(validate(address.pop())) #city
        output.append(state) #state
        output.append(zipcode) #zipcode
        output.append(get_value(country_code)) #country code
        output.append(get_value(name.xpath('./@data-nid'))) #store_number
        output.append(get_value(store.xpath('.//div[@class="result-item-phone"]//text()')).replace('Phone: ', '')) #phone
        output.append("MAGNIFICENT DIAMOND JEWELRY SHOP") #location type
        output.append(get_value(geoinfo.split(', ')[0])) #latitude
        output.append(get_value(geoinfo.split(', ')[1])) #longitude
        output.append(get_value(hours)) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
