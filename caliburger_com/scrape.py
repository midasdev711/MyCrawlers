import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://caliburger.com'

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
    url = "https://caliburger.com/locations"
    request = requests.get(url)
    response = request.text.split('United States</div>')[1].split('<div id="cali-country-Mexico"')[0]
    response = etree.HTML(response)
    store_list = response.xpath('//div[@id="us-accordion"]')
    for store in store_list:
        info = validate(eliminate_space(store.xpath('.//text()')))
        if 'COMING SOON' in info:
            continue
        title = validate(store.xpath('.//div[contains(@class, "cali-store-name")]//td')[0].xpath('.//text()'))
        address = eliminate_space(store.xpath('.//div[@class="cali-store-address"]//text()'))
        geoinfo = validate(store.xpath('.//iframe/@src')).split('!2d')[1]
        latitude = geoinfo.split('!3d')[0]
        longitude = geoinfo.split('!3d')[1].split('!')[0]
        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(validate(address[:-1])) #address
        output.append(address[-1:][0].split(' ').pop(0)) #city
        output.append(address[-1:][0].split(' ')[:-1].pop()) #state
        output.append(address[-1:][0].split(' ').pop()) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append("<MISSING>") #phone
        output.append("Southern California style burgers - CaliBurger: Always Fresh") #location type
        output.append(latitude) #latitude
        output.append(longitude) #longitude
        output.append("<MISSING>") #opening hours

        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
