import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.sunriserecords.com'

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

    url = "https://www.sunriserecords.com/locations/"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[@class="vc_tta-panel"]')

    for store_block in store_list:

        state = validate(store_block.xpath('.//span[@class="vc_tta-title-text"]//text()'))
        store_data = store_block.xpath('.//tr')

        for store in store_data:
            title = validate(store.xpath(".//td")[0].xpath(".//text()"))
            if "NOW CLOSED" in title:
                continue
            info = validate(store.xpath(".//td//text()")[1]).split(',')
            street = info[0]
            if len(info) < 2:
                if '-' in info[0]:
                    zipcode = "<MISSING>"
                else:
                    zipcode = info[0][-6:]
            else:
                zipcode = info.pop()
                if len(zipcode.split(' ')) > 3:
                    zipcode = validate(zipcode.split(' ')[2:])

            
            city = validate(store.xpath(".//td//text()")[2])
            phone = validate(store.xpath(".//td//text()")[3])
            geoinfo = validate(store.xpath(".//td/a/@href")).split('@')
            if len(geoinfo) < 2:
                geoinfo = ["<MISSING>", "<MISSING>"]
            else:
                geoinfo = geoinfo[1].split(',')[:2]

            output = []
            output.append(base_url) # url
            output.append(title) #location name
            output.append(street) #address
            output.append(city) #city
            output.append(state) #state
            output.append(zipcode) #zipcode
            output.append('CA') #country code
            output.append("<MISSING>") #store_number
            output.append(phone) #phone
            output.append("Sunrise Records - Leading Canadian retailer of music, film, games, and pop culture items") #location type
            output.append(geoinfo[0]) #latitude
            output.append(geoinfo[1]) #longitude
            output.append("<MISSING>") #opening hours

            output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
