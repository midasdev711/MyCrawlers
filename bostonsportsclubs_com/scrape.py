import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.bostonsportsclubs.com'

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
    url = "https://www.bostonsportsclubs.com/clubs"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_url_list = response.xpath('//div[@class="club-locations"]//a/@href')
    store_url_list.append(url)
    for store_url in store_url_list:
        store_request = requests.get(store_url)
        store_list = etree.HTML(store_request.text).xpath('.//ul[@id="map-club-accordion"]//li[contains(@class, "club-detail")]')
        store_json = json.loads(store_request.text.split('clubs = ')[1].split(';')[0])
        geoinfo = {}
        for x in store_json:
        	geoinfo[x['code']] = {"latitude": x['latitude'], "longitude": x['longitude']}
        for store in store_list:
        	detail_url = store.xpath('.//a/@href')[0]
        	detail_request = requests.get(store_url[:-6] + detail_url)
        	detail = etree.HTML(detail_request.text)
        	hours = get_value(eliminate_space(detail.xpath('.//table[@class="table-condensed"]//text()')))
        	store_id = validate(store.xpath('./@data-code'))

	        output = []
	        output.append(store_url[:-6]) # url
	        output.append(validate(detail.xpath('.//h1[@itemprop="name"]//text()'))) #location name
	        output.append(validate(detail.xpath('.//span[@itemprop="streetAddress"]//text()'))) #address
	        output.append(validate(detail.xpath('.//span[@itemprop="addressLocality"]//text()'))) #city
	        output.append(get_value(detail.xpath('.//span[@itemprop="addressRegion"]//text()'))) #state
	        output.append(validate(detail.xpath('.//span[@itemprop="postalCode"]//text()'))) #zipcode
	        output.append('US') #country code
	        output.append(store_id) #store_number
	        output.append(validate(detail.xpath('.//span[@itemprop="telephone"]//text()'))) #phone
	        output.append("Sports Clubs | Fitness that Fits") #location type
	        output.append(geoinfo[store_id]['latitude']) #latitude
	        output.append(geoinfo[store_id]['longitude']) #longitude
	        output.append(hours) #opening hours
	        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
