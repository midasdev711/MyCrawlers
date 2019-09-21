import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.freshtoorder.com'

def validate(item):
    if type(item) == list:
        item = ' '.join(item)
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
    url = "https://www.freshtoorder.com/locate/"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = json.loads(request.text.split('search_radius, ')[1].split(', map_instance,')[0])
    store_json = {}
    for x in store_list:
        store_json[validate(str(x['ID']))] = x
    store_texts = response.xpath('//div[contains(@class, "mpfy-mll-location")]')
    for store_text in store_texts:
        store = store_json[validate(store_text.xpath('./@data-id'))]
        info = validate(store_text.xpath('.//div[contains(@class, "location-address")]//text()')).split('|')
        info = info.pop().split(',')
        hours = get_value(eliminate_space(store_text.xpath('.//div[contains(@class, "location-hours")]//text()'))).replace('\n', '').replace('Restaurant Hours: ', '').replace('OPEN NOW!!! ', '')
        if 'Closed' in hours:
            continue
        street_info = eliminate_space(etree.HTML(store['tooltip_content']).xpath('.//text()'))
        street = street_info[1]
        if 'OPEN' in street:
            street = street_info[2]
        else:
            if 'Suite' in street or 'Leon' in street or 'Parkway' in street:
                street = street_info[1]
            else:
                street = street_info[1] + ' ' + street_info[2]
        output = []
        output.append(base_url) # url
        output.append(validate(store['post_title'])) #location name
        output.append(validate(street)) #address
        output.append(validate(store['pin_city'])) #city
        output.append(info[1]) #state
        output.append(validate(store['pin_zip'])) #zipcode
        output.append('US') #country code
        output.append(store['ID']) #store_number
        output.append(get_value(store_text.xpath('.//div[contains(@class, "contact-details")]//text()'))) #phone
        output.append("Fresh To Order") #location type
        output.append(validate(store['google_coords'][0])) #latitude
        output.append(validate(store['google_coords'][1])) #longitude
        output.append(hours) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
