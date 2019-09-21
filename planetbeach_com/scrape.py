import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://planetbeach.com'

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
    url = "https://planetbeach.com/spa-locator/"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "_ga=GA1.2.1396633512.1567671898; _gid=GA1.2.1689612863.1567671898; PHPSESSID=9547a9f50e8fa8996e962a86623cedcc; _fbp=fb.1.1567671900949.165584815; _gat=1",
        "referer": "https://planetbeach.com/",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    request = requests.get(url, headers=headers)
    response = etree.HTML(request.text)
    store_url_list = response.xpath('//ul[@class="bottomLocations"]//a/@href')
    for store_url in store_url_list:
        detail_request = requests.get(store_url, headers=headers)
        store = etree.HTML(detail_request.text)
        geoinfo = validate(store.xpath(".//div[@class='hidden-md hidden-lg']/@style")).split('red%7C')[1].split("')")[0].split(',')
        hours = validate(eliminate_space(store.xpath('.//div[@class="map-hours"]//div//text()'))).replace('\n', '') + validate(eliminate_space(store.xpath('.//div[@class="map-hours"]//h5//text()'))).replace('\n', '')

        output = []
        output.append(base_url) # url
        output.append(validate(store.xpath(".//span[@id='spaName']//text()"))) #location name
        output.append(validate(store.xpath(".//span[@itemprop='streetAddress']//text()"))) #address
        output.append(validate(store.xpath(".//span[@itemprop='addressLocality']//text()"))) #city
        output.append(validate(store.xpath(".//span[@itemprop='addressRegion']//text()"))) #state
        output.append(validate(store.xpath(".//span[@itemprop='postalCode']//text()"))) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append(validate(store.xpath(".//span[@itemprop='telephone']//text()"))) #phone
        output.append("Planet Beach spray and spa") #location type
        output.append(geoinfo[0]) #latitude
        output.append(geoinfo[1]) #longitude
        output.append(hours) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
