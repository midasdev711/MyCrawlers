import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.hcoafitness.com'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    while True:
        if item[-1:] == ' ':
            item = item[:-1]
        else:
            break
    return item.replace(u'\u2013', '-').encode('ascii', 'ignore').encode("utf8").strip()

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
    url = "https://www.hcoafitness.com/en/locations"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = json.loads(request.text.split('$("#map1").maps(')[1].split(').data')[0])['places']

    store_htmls = response.xpath('.//div[contains(@class, "location-box")]')
    store_data = {}
    for store_html in store_htmls:
        detail_url = validate(store_html.xpath(".//a/@href")[0])
        detail_request = requests.get(detail_url)
        detail = etree.HTML(detail_request.text)
        phone = get_value(eliminate_space(detail.xpath('.//span[contains(@class, "page-caption-phone-mobile")]//text()')))
        title = 'HCOA Fitness ' + get_value(detail.xpath('.//h1[@class="infinite-page-title"]//text()'))
        hours = validate(eliminate_space(detail.xpath('.//text()'))).split('Horarios')[1].split('Itinerario de Clases')[0]
        address = validate(eliminate_space(store_html.xpath('.//div[@class="gdlr-core-feature-box-item-content"]/p//text()'))[:2])
        store_data[title] = {"phone": phone, "hours": hours, "address": address}

    for store in store_list:   
        title = validate(store['title'])
        if not store_data.get(title):
            index = 'HCOA Fitness Rexville'
        else:
            index = title
        address = store_data[index]["address"]
        output = []
        output.append(base_url) # url
        output.append(title.replace('HCOA Fitness ', '')) #location name
        output.append(address) #address
        output.append(validate(store['location']['city'])) #city
        output.append(validate(store['location']['state'])) #state
        output.append(validate(store['location']['postal_code'])) #zipcode
        output.append(validate(store['location']['country'])) #country code
        output.append(validate(store['id'])) #store_number
        
        output.append(store_data[index]['phone']) #phone
        output.append("HCOA Fitness") #location type
        output.append(validate(store['location']['lat'])) #latitude
        output.append(validate(store['location']['lng'])) #longitude
        output.append(store_data[index]['hours']) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
