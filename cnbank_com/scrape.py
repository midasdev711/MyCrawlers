import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.cnbank.com'

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
    url = "https://www.cnbank.com/locations.aspx"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//table[contains(@class, "branch-list")]//a[@class="link-blk_new"]')
    for store in store_list:
        title = validate(store.xpath(".//text()"))
        detail_url = validate(store.xpath("./@href"))
        detail_request = requests.get(base_url + detail_url)
        detail = etree.HTML(detail_request.text)

        info = detail.xpath("//div[contains(@class, 'interiorContainer')]//div[@class='grid_4']//p//text()")
        phone = info.pop()
        info = info[:-2]
        citystatezip = validate(info.pop())
        address = get_value(info).replace('(mailing address)', '')
        geoinfo = detail_request.text.split('center: new google.maps.LatLng(')[1].split('zoom')[0]
        latitude = validate(geoinfo.split(', ')[0])
        longitude = validate(geoinfo.split(', ')[1].split(')')[0])
        hours = get_value(eliminate_space(detail.xpath(".//table[@class='branchTable']//text()")))

        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(address) #address
        output.append(citystatezip.split(', ')[0]) #city
        output.append(citystatezip.split(', ')[1][:2]) #state
        output.append(citystatezip.split(', ')[1][2:]) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append(phone) #phone
        output.append("Canandaigua National Bank & Trust") #location type
        output.append(latitude) #latitude
        output.append(longitude) #longitude
        output.append(hours) #opening hours

        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
