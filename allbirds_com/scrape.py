import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.allbirds.com'

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
    url = "https://www.allbirds.com/pages/stores"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[@class="positioner"]')
    for store in store_list:
        title = validate(store.xpath(".//h2[@class='t-second-header']//text()"))
        info = store.xpath(".//p[@class='t-content-paragraph']")[1]
        address = info.xpath('.//text()')
        street_address = validate(address[0])
        city_state_zip = validate(address[1])
        state = city_state_zip.split(', ')[1]
        if state == "UK":
            city_state_zip = city_state_zip.split(', ')[0].split(' ')
            city = city_state_zip.pop(0)
            zipcode = get_value(city_state_zip)
            country = "UK"
        else:
            city = city_state_zip.split(', ')[0]
            zipcode = '<MISSING>'
            country = "US"
        if len(state) > 2:
            state = state.split(' ')
            zipcode = state.pop()
            state = validate(state)
        phone = validate(store.xpath('.//text()'))
        regex = r"(\d{3}-\d{3}-\d{4})"
        phone = re.findall(regex, phone)
        if len(phone) > 0:
            phone = validate(phone)
        else:
            phone = "<MISSING>"

        geoinfo = validate(info.xpath('.//a/@href'))
        geoinfo = geoinfo.split('@')
        latitude = ""
        longitude = ""
        if len(geoinfo) > 1:
            latitude = geoinfo[1].split(',')[0]
            longitude = geoinfo[1].split(',')[1]
        else:
            latitude = '<MISSING>'
            longitude = '<MISSING>'
        hours = get_value(eliminate_space(store.xpath(".//p[@class='t-content-paragraph']")[2].xpath('.//text()')))

        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(street_address) #address
        output.append(city) #city
        output.append(state) #state
        output.append(zipcode) #zipcode
        output.append(country) #country code
        output.append("<MISSING>") #store_number
        output.append(phone) #phone
        output.append("Allbirds - Shop for boots, shocks and accessories") #location type
        output.append(latitude) #latitude
        output.append(longitude) #longitude
        output.append(hours) #opening hours

        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
