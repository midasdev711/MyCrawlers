import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'http://mariaempanada.com'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').encode("utf8").strip().replace('\n', '')

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
    url = "http://mariaempanada.com/contact/"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://lamadeleine.com/locations",
        "Sec-Fetch-Mode": "cors",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    response = etree.HTML(requests.get(url).text)
    sections = response.xpath('//div[contains(@class, "grid_section")]')
    store_list = []
    for x in xrange(0,2):
        store_list += sections[x].xpath('.//div[contains(@class, "vc_col-sm-4")]//div[@class="vc_column-inner "]')
    store_list = store_list[:-1]
    for store in store_list:
        title = store.xpath(".//div[contains(@class, 'wpb_text_column')]")[0].xpath('.//h4/text()')[0]
        street_address = store.xpath(".//div[contains(@class, 'wpb_text_column')]")[1].xpath('.//p//text()')[0]
        address = store.xpath(".//div[contains(@class, 'wpb_text_column')]")[1].xpath('.//p//text()')[1]
        phone = store.xpath(".//div[contains(@class, 'wpb_text_column')]")[1].xpath('.//p//text()')[3]
        store_hours = store.xpath(".//div[contains(@class, 'wpb_text_column')]")[1].xpath('.//p//text()')[5]
        location_type = store.xpath(".//div[contains(@class, 'wpb_text_column')]")[0].xpath('.//h6/text()')[0]
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
        if 'X' in phone:
            phone = "<MISSING>"

        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(street_address) #address
        output.append(validate(city)) #city
        output.append(validate(state)) #state
        output.append(validate(zipcode)) #zipcode
        output.append('US') #country code
        output.append('<MISSING>') #store_number
        output.append(phone) #phone
        output.append(location_type) #location type
        output.append('<INACCESSIBLE>') #latitude
        output.append('<INACCESSIBLE>') #longitude
        output.append(get_value(store_hours)) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
