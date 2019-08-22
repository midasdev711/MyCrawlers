import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'http://www.fourbrotherspizzainn.com'

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
    url = "http://www.fourbrotherspizzainn.com/locations/"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[contains(@class, "palm-one-whole")]')
    for store in store_list:

        info = eliminate_space(store.xpath("./p//text()"))

        output = []
        output.append(base_url) # url
        output.append(get_value(store.xpath(".//h5/text()"))) #location name
        output.append(info[0]) #address
        output.append(info[1].split(', ')[0].replace('\n', '')) #city
        output.append(info[1].split(', ')[1].split(' ')[0]) #state
        output.append(info[1].split(', ')[1].split(' ')[1]) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append(info[2]) #phone
        output.append("The Four Stefanopoulos Brothers Pizza Restaurant") #location type
        output.append('<MISSING>') #latitude
        output.append('<MISSING>') #longitude
        output.append('<MISSING>') #opening hours

        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
