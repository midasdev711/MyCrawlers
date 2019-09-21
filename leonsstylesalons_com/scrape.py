import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'http://www.leonsstylesalons.com'

def validate(item):
    if type(item) == list:
        item = ' '.join(item)
    while True:
        if item[-1:] == ' ':
            item = item[:-1]
        else:
            break
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
    url = "http://www.leonsstylesalons.com/locations"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_url_list = response.xpath('//article//a/@href')[1:]
    for store_url in store_url_list:
        store = etree.HTML(requests.get(store_url).text)
        address = eliminate_space(store.xpath(".//div[@class='entry-content']//p")[0].xpath(".//text()"))
        hours = get_value(store.xpath(".//div[@class='entry-content']//p")[1].xpath(".//text()"))
        output = []
        output.append(base_url) # url
        output.append(validate(store.xpath('.//header[@class="entry-header"]//text()'))) #location name
        output.append(address[0]) #address
        output.append(address[1].split(', ')[0]) #city
        output.append(address[1].split(', ')[1].split(' ')[0]) #state
        output.append(address[1].split(', ')[1].split(' ')[1]) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append(address[2].replace('Phone: ', '')) #phone
        output.append("Leon's Style Salons") #location type
        output.append("<MISSING>") #latitude
        output.append("<MISSING>") #longitude
        output.append(hours.replace('\n', '')) #opening hours

        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
