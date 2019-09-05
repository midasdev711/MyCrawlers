import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.fabletics.com'

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
    url = "https://www.fabletics.com/store-locations"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[@class="store-location "]')
    for store in store_list:
        status = get_value(store.xpath(".//span[@class='store-location-announcement']//text()"))
        if status == "COMING SOON!":
            continue

        title = validate(store.xpath(".//div[@class='store-location-heading-name']//text()"))

        address = eliminate_space(store.xpath('.//div[@class="store-location-address-line"]//text()'))

        city_state_zip = address.pop()
        city = city_state_zip.split(',')[0]
        state = city_state_zip.split(', ')[1].split(' ')[0]
        zipcode = city_state_zip.split(', ')[1].split(' ')[1]
        street = get_value(address)

        phone = validate(store.xpath('.//div[@class="store-location-phone"]//a//text()'))
        hours = get_value(eliminate_space(store.xpath('.//dl[contains(@class, "store-location-hours")]//text()')))
        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(street) #address
        output.append(city) #city
        output.append(state) #state
        output.append(zipcode) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append(phone) #phone
        output.append("Fabletics - Activewear, Fitness & Workout Clothes Store") #location type
        output.append("<MISSING>") #latitude
        output.append("<MISSING>") #longitude
        output.append(hours) #opening hours

        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
