import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.stonewoodgrill.com'

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
    url = "https://www.stonewoodgrill.com/locations/index"
    request = requests.get(url)
    response = request.text.split('var arrGeoLocation=')[1].split('var reloadOnFind=false;')[0][:-2]
    store_list = json.loads(response)
    for store in store_list:
        address = eliminate_space(etree.HTML(store['html']).xpath('.//div[contains(@class, "location-address")]//text()'))
        phone = validate(etree.HTML(store['html']).xpath('.//div[contains(@class, "location-phone")]//text()'))
        detail_url = validate(etree.HTML(store['html']).xpath('.//a[contains(@class, "more-info")]/@href'))
        detail = etree.HTML(requests.get(base_url + detail_url).text)
        hours = get_value(detail.xpath('.//div[contains(@class, "location-info")]//div[@class="zEditorHTML"]')[0].xpath('.//text()'))
        output = []
        output.append(base_url) # url
        output.append(validate(store['name'])) #location name
        output.append(address[0]) #address
        output.append(address[1].split(', ')[0]) #city
        output.append(address[1].split(', ')[1].split(' ')[0]) #state
        output.append(address[1].split(', ')[1].split(' ')[1]) #zipcode
        output.append(validate('US')) #country code
        output.append(validate(store['id'])) #store_number
        output.append(phone) #phone
        output.append("Steakhouse and Seafood | Stonewood Grill & Tavern") #location type
        output.append(validate(store['latitude'])) #latitude
        output.append(validate(store['longitude'])) #longitude
        output.append(hours.replace('\n', '')) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
