import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://bookmans.com'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    while True:
        if item[-1:] == ' ':
            item = item[:-1]
        else:
            break
    return item.replace(u'\u2014', '-').encode('ascii', 'ignore').encode("utf8").strip()

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
    url = "https://bookmans.com/#stores"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[contains(@class, "sh-accordion-item")]')

    hours = ""
    hours += get_value(response.xpath('//div[@class="footer-inner"]//h2//text()'))
    hours += get_value(eliminate_space(response.xpath('//div[@class="footer-hours"]//text()')))
    for store in store_list:
        title = get_value(store.xpath(".//span[@class='sh-accordion-title']//text()"))
        address_info = eliminate_space(store.xpath(".//div[@class='fw-page-builder-content']//text()"))

        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(address_info[1]) #address
        output.append(address_info[2].split(', ')[0]) #city
        output.append(address_info[2].split(', ')[1].split(' ')[0]) #state
        output.append(address_info[2].split(', ')[1].split(' ')[1]) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append(address_info[3]) #phone
        output.append("Bookmans Entertainment Exchange") #location type
        output.append('<INACCESSIBLE>') #latitude
        output.append("<INACCESSIBLE>") #longitude
        output.append(hours) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
