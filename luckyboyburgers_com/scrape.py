import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress

base_url = 'http://luckyboyburgers.com'

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

def parse_address(address):
    address = usaddress.parse(address)
    street = ''
    city = ''
    state = ''
    zipcode = ''
    country = ''
    for addr in address:
        if addr[1] == 'PlaceName':
            city += addr[0].replace(',', '') + ' '
        elif addr[1] == 'ZipCode':
            zipcode = addr[0].replace(',', '')
        elif addr[1] == 'StateName':
            state = addr[0].replace(',', '')
        elif addr[1] == 'CountryName':
            country = addr[0].replace(',', '')
        else:
            street += addr[0].replace(',', '') + ' '

    return { 
            'street': get_value(street), 
            'city' : get_value(city), 
            'state' : get_value(state), 
            'zipcode' : get_value(zipcode),
            'country': get_value(country)
            }

def fetch_data():
    output_list = []
    url = "http://luckyboyburgers.com/location"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[@class="sqs-block-content"]')
    store_list = [store_list[1], store_list[3]]
    for store in store_list:
        info = eliminate_space(store.xpath(".//text()"))
        geoinfo = validate(store.xpath(".//a/@href"))
        address = parse_address(info.pop())
        title = info.pop(0).split(' ')[0]
        latitude = geoinfo.split('sll=')[1].split(',')[0]
        longitude = geoinfo.split('sll=')[1].split(',')[1].split('&')[0]

        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(address['street']) #address
        output.append(address['city']) #city
        output.append(address['state']) #state
        output.append(address['zipcode']) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append('<MISSING>') #phone
        output.append("Lucky Boy Burgers") #location type
        output.append(latitude) #latitude
        output.append(longitude) #longitude
        output.append(validate(info)) #opening hours

        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
