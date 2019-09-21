import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'http://kingtaco.com'

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
    url = "http://kingtaco.com/locations.html"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//article')[1:-5]
    for store in store_list:
        address = eliminate_space(store.xpath('.//div[@class="caption"]//text()'))
        geoinfo = validate(store.xpath('.//div[@class="caption"]//a/@href'))
        latitude = geoinfo.split('!2d')[1].split('!3d')[0]
        longitude = geoinfo.split('!3d')[1].split('!')[0]
        if len(address) <= 2:
            phone = "<MISSING>"
        else:
            phone = address[2]

        output = []
        output.append(base_url) # url
        output.append(validate(store.xpath(".//h3//text()"))) #location name
        output.append(address[0]) #address
        output.append(address[1].split(', ')[0]) #city
        output.append(address[1].split(', ')[1][:2]) #state
        output.append(address[1].split(', ')[1][3:]) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append(phone.replace('Phone: ', '')) #phone
        output.append("King Taco Restaurant - Mexican Food") #location type
        output.append(latitude) #latitude
        output.append(longitude) #longitude
        output.append(get_value(address[3:])) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
