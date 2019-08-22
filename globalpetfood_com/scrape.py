import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://globalpetfoods.com/'

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
    url = "https://globalpetfoods.com/store-locations/?user_location=&search=Search#"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[@class="store_list_item"]')

    geoinfo_tmp = request.text.split('position: ')
    geoinfo = {}
    for x in xrange(2, len(geoinfo_tmp)):
        tmp = validate(geoinfo_tmp[x].split('icon: ')[0])
        lat = tmp.split('lat: ')[1].split(',')[0]
        lng = tmp.split('lng: ')[1].split('}')[0]
        title = validate(tmp.split("title: '")[1].split("'")[0])
        geoinfo[title] = {"lat": lat, "lng": lng}

        
    for store in store_list:
        detail_url = store.xpath(".//span[@class='single_location_title']/a/@href")[0]
        detail_request = requests.get(detail_url)
        detail = etree.HTML(detail_request.text)

        title = get_value(detail.xpath(".//span[@class='location_title']//text()"))

        address_info = get_value(detail.xpath(".//span[@class='location_address']//text()")[1]).split(', ')

        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(get_value(detail.xpath(".//span[@class='location_address']//text()")[0])) #address
        output.append(address_info[0]) #city
        output.append(address_info[1]) #state
        output.append(address_info[2]) #zipcode
        output.append('CA') #country code
        output.append("<MISSING>") #store_number
        output.append(get_value(detail.xpath(".//span[@class='location_phone']//text()"))) #phone
        output.append("The largest Canadian-owned pet specialty retailer") #location type
        output.append(geoinfo[title]['lat']) #latitude
        output.append(geoinfo[title]['lng']) #longitude
        output.append(get_value(detail.xpath(".//span[@class='location_hours_full']//text()")).replace('\n', '')) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
