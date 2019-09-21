import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'http://www.planetbeachcanada.com'

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
    url = "http://www.planetbeachcanada.com/wp-content/plugins/planetbeach-store-locator/api/archive-getter.php"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_url_list = response.xpath('//div[@class="col-sm-4"]/a/@href')
    for store_url in store_url_list:
        detail_request = requests.get(store_url)
        store = etree.HTML(detail_request.text)

        address = eliminate_space(store.xpath('//div[@class="col-md-3"]')[0].xpath('.//text()'))[1:]
        if 'Email:' in address:
            address = address[:-2]
        if len(address) == 0:
            phone = "<MISSING>"
            city = "<MISSING>"
            state = "<MISSING>"
            zipcode = "<MISSING>"
            street_address = "<MISSING>"
        else:
            phone = address.pop()
            city_state_zip = address.pop()
            city = city_state_zip.split(',')[0]
            state = city_state_zip.split(', ')[1][:2]
            zipcode = city_state_zip.split(', ')[1][3:]
            street_address = validate(address)

        geoinfo = store.xpath(".//div[@class='marker']")[0]
        hours = eliminate_space(store.xpath('//div[@class="col-md-3"]')[1].xpath('.//text()'))[1:]

        output = []
        output.append(base_url) # url
        output.append(validate(store.xpath(".//h1")[0].xpath(".//text()"))) #location name
        output.append(street_address) #address
        output.append(city) #city
        output.append(state) #state
        output.append(zipcode) #zipcode
        output.append('CA') #country code
        output.append("<MISSING>") #store_number
        output.append(phone.replace('Phone: ', '')) #phone
        output.append("Planet Beach spray and spa") #location type
        output.append(get_value(geoinfo.xpath('./@data-lat'))) #latitude
        output.append(get_value(geoinfo.xpath('./@data-lng'))) #longitude
        output.append(get_value(hours)) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
