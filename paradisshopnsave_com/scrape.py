import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'https://paradisshopnsave.com'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').encode("utf8").strip().replace('\n', '').replace('\t', '')

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
    url = "https://paradisshopnsave.com/location"
    request = requests.get(url)
    response = etree.HTML(request.text.encode("utf-8"))
    store_list = response.xpath('//div[@class="location-shop"]')
    for store in store_list:
        title = validate(store.xpath('.//div[@class="location-shop-title"]/text()'))
        location_address = store.xpath('.//div[@class="location-address"]/text()')
        hours_url = store.xpath('.//div[@class="store-hours"]/a/@href')[0]
        detailrequest = requests.get(hours_url)
        detail = etree.HTML(detailrequest.text.encode("utf-8"))
        hour_table = detail.xpath('//table')
        store_hours = ""

        # store_hours in the first table
        store_hours += validate(hour_table[0].xpath('.//tr')[0].xpath(".//text()")) + ':'
        label_list = hour_table[0].xpath(".//tr")[1].xpath('.//td//text()')
        new_label_list = []
        for x in xrange(0, len(label_list) / 2):
            new_label_list.append(label_list[x * 2] + ' ' + label_list[(x * 2) + 1])

        hour_list = hour_table[0].xpath(".//tr")[2].xpath('.//td//text()')
        for idx, item in enumerate(new_label_list):
            store_hours += validate(item + ':' + hour_list[idx]) + ' '

        # store_hours in the second table

        store_hours += validate(hour_table[1].xpath('.//tr')[0].xpath(".//text()")) + ':'
        labels = hour_table[1].xpath(".//tr")[1].xpath('.//td')
        label_list = []
        for x in labels:
            label_list.append(get_value(x.xpath(".//text()")))
        hour_list = hour_table[1].xpath(".//tr")[2].xpath('.//td')
        hours = []
        for x in hour_list:
            hours.append(get_value(x.xpath('.//text()')))
        for idx, item in enumerate(label_list):
            store_hours += validate(item + ':' + hours[idx].replace('\n', '')) + ' '

        location_address = eliminate_space(location_address)
        province = location_address[1].split(',')
        
        address = validate(location_address[0])
        city = validate(province[0])
        state = validate(province[1].split(' ')[1])
        zipcode = validate(province[1].split(' ')[2])
        phone = location_address[2]

        output = []
        output.append(base_url) # url
        output.append(validate(store.xpath('.//div[@class="location-shop-title"]/text()'))) #location name
        output.append(address) #address
        output.append(city) #city
        output.append(state) #state
        output.append(zipcode) #zipcode
        output.append('US') #country code
        output.append('<MISSING>') #store_number
        output.append(phone) #phone
        output.append("Paradis Shop'n Save-Supermarkets") #location type
        output.append('<MISSING>') #latitude
        output.append('<MISSING>') #longitude
        output.append(get_value(store_hours).replace('N/A', '<MISSING>')) #opening hours
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
