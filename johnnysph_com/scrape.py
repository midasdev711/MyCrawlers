import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'https://johnnysph.com'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').encode("utf8").strip().replace('Hours', '')

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
    url = "https://johnnysph.com/locations/?post%5B0%5D=jph_store&address%5B0%5D&gmw_distance=100&units=imperial&per_page=100&lat&lng&form=2"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_html = response.xpath('.//div[@class="locations "]')
    store_list = json.loads(request.text.split('var gmwMapObjects = ')[1].split('/* ]]> */')[0][:-2])
    for idx, store in store_list.items():
        store = store['locations'][0]
        info = etree.HTML(store['info_window_content'])
        title = validate(info.xpath('.//a//text()'))
        original_address = validate(info.xpath('.//span[@class="address"]//text()'))
        address = parse_address(original_address)
        detail_url = validate(info.xpath('.//a/@href'))
        detail_request = requests.get(detail_url)
        detail = etree.HTML(detail_request.text)

        html_info = get_value(response.xpath('.//a[contains(@href, "' + detail_url + '")]')[0].xpath(".//text()"))
        if address['street'] == "<MISSING>":
            address['street'] = html_info.split(', ')[0]
            address['state'] = original_address.split(', ')[1]
            address['country'] = original_address.split(', ').pop()
        store_hours = get_value(eliminate_space(detail.xpath('.//div[@class="hours"]//text()')))

        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(validate(address['street'])) #address
        output.append(validate(address['city'])) #city
        output.append(validate(address['state'])) #state
        output.append(validate(address['zipcode'])) #zipcode
        output.append(validate(address['country'])) #country code
        output.append(validate(idx)) #store_number
        output.append("<MISSING>") #phone
        output.append("Pizza locations in Louisiana - Johnny's Pizza House") #location type
        output.append(validate(store["lat"])) #latitude
        output.append(validate(store["lng"])) #longitude
        output.append(store_hours) #opening hours  
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
