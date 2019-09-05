import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'https://www.jmclaughlin.com'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').encode("utf8").strip()

def get_value(item):
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
    url = "https://www.jmclaughlin.com/storelocator/view/storelist"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[@class="location-stores"]//div[contains(@class, "grid-12")]/div')
    for store in store_list:
        address = get_value(store.xpath('.//div[@class="store_name"]/text()')[2])
        address = usaddress.parse(address)
        street = ''
        city = ''
        state = ''
        zipcode = ''
        for addr in address:
            if addr[1] == 'PlaceName':
                city += addr[0].replace(',', '') + ' '
            elif addr[1] == 'ZipCode':
                zipcode = addr[0]
            elif addr[1] == 'StateName':
                state = addr[0]
            else:
                street += addr[0].replace(',', '') + ' '
        if city == "":
            city = address[0][0] + ' ' + address[1][0]
            city = city[:-1]
        store_hours = get_value(store.xpath('.//div[@class="list-store-time"]//text()')).replace("\n", "").replace("  ", '')
        geo = store.xpath('.//div[@class="stores_list_item__bottom"]//a')[0].xpath('./@href')[0].split('q=')[1].split(',')
        output = []
        output.append(base_url) # url
        output.append(get_value(store.xpath('.//div[@class="store_name"]/text()')[0])) #location name
        output.append(get_value(store.xpath('.//div[@class="store_name"]/text()')[1])) #address
        output.append(get_value(city)) #city
        output.append(get_value(state)) #state
        output.append(get_value(zipcode)) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append(get_value(store.xpath('.//div[@class="phone"]//text()'))) #phone
        output.append("Cloth and Accessory Shop") #location type
        output.append(get_value(geo[0])) #latitude
        output.append(get_value(geo[1])) #longitude
        output.append(store_hours) #opening hours  
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
