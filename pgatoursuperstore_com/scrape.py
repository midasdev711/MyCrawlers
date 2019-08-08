import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.pgatoursuperstore.com'

def write_output(data):
    with open('data.csv', mode='w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["locator_domain", "location_name", "street_address", "city", "state", "zip", "country_code", "store_number", "phone", "location_type", "latitude", "longitude", "hours_of_operation"])
        for row in data:
            writer.writerow(row)
    return

def fetch_data():
    output_list = []
    url = "https://www.pgatoursuperstore.com/stores"
    request = requests.get(url)
    response = etree.HTML(request.text.encode("utf-8"))
    store_list = response.xpath('//div[@class="store"]')
    for store in store_list:
        output = []
        city_state_zip = store.xpath('.//div[@class="cityStateZip"]/text()')[0]
        city = city_state_zip.split(',')[0]
        state = city_state_zip.split(',').pop().split(' ')[1]
        zipcode = city_state_zip.split(',').pop().split(' ')[2]
        hours = store.xpath('.//div[@class="hours"]/text()')
        store_hours = "".join(hours)
        output.append(base_url)
        output.append(store.xpath('.//div[@class="storename"]//a//span/text()')[0])
        output.append(store.xpath('.//div[@class="address1"]/text()')[0])
        output.append(city)
        output.append(state)
        output.append(zipcode)
        output.append('US')
        output.append(store.xpath('./@id')[0])
        output.append(store.xpath('.//div[@class="phone"]//a/text()')[0])
        output.append('PGA Tour Superstore')
        output.append('<MISSING>')
        output.append('<MISSING>')
        output.append(store_hours.replace('\n', ''))
        output_list.append(output)
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
