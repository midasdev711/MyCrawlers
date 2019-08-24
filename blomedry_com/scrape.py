import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://blomedry.com'

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
    url = "https://blomedry.com/locations/"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//article')

    geoinfo_tmp = json.loads(request.text.split('var mapdeatils = ')[1].split(';')[0])
    geoinfo = {}
    for tmp in geoinfo_tmp:
        lat = validate(tmp[1])
        lng = validate(tmp[2])
        title = validate(tmp[0])
        geoinfo[title] = {"lat": lat, "lng": lng}

    for store in store_list:
        highlight = store.xpath(".//p[@class='location-highlight']//text()")
        if len(highlight) > 0 and validate(highlight) == "coming soon!":
            continue
        detail_url = get_value(store.xpath(".//h3[contains(@class, 'entry-title')]/a/@href"))
        detail_request = requests.get(detail_url)
        detail = etree.HTML(detail_request.text)

        title = get_value(store.xpath(".//h3[contains(@class, 'entry-title')]//text()"))

        address = store.xpath(".//p[@class='location-address']//text()")
        hours = get_value(highlight or detail.xpath(".//p[contains(@class, 'location-hours')]//text()")).replace('\n', '')

        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(get_value(address[0])) #address
        output.append(get_value(address[1]).split(' ')[0]) #city
        output.append(get_value(address[1]).split(' ')[1]) #state
        output.append(get_value(address[2])) #zipcode
        output.append('CA') #country code
        output.append("<MISSING>") #store_number
        output.append(get_value(store.xpath(".//span[contains(@class, 'phone')]//text()"))) #phone
        output.append("The Original Blow Dry Bar | Blo Blow Dry Bar") #location type
        output.append(geoinfo[title]['lat']) #latitude
        output.append(geoinfo[title]['lng']) #longitude
        output.append(hours) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
