import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress

base_url = 'https://www.wyndhamhotels.com'

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

def parse_address(address):
    address = usaddress.parse(address)
    street = ''
    city = ''
    state = ''
    zipcode = ''
    country = ''
    for addr in address:
        if addr[1] == 'PlaceName':
            city += addr[0].replace(',', '') + ' '
        elif addr[1] == 'ZipCode':
            zipcode = addr[0].replace(',', '')
        elif addr[1] == 'StateName':
            state = addr[0].replace(',', '')
        elif addr[1] == 'CountryName':
            country = addr[0].replace(',', '')
        else:
            street += addr[0].replace(',', '') + ' '

    return { 
            'street': get_value(street), 
            'city' : get_value(city), 
            'state' : get_value(state), 
            'zipcode' : get_value(zipcode),
            'country': get_value(country)
            }

def fetch_data():
    output_list = []
    url = "https://www.wyndhamhotels.com/americinn/locations"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[@class="state-container"]//li[@class="property"]')
    for detail_url in store_list:
        detail_url = validate(detail_url.xpath('.//a')[0].xpath('./@href'))
        detail_request = requests.get('https://www.wyndhamhotels.com' + detail_url)
        detail = etree.HTML(detail_request.text)

        address = validate(detail.xpath('.//div[contains(@class, "property-address")]//text()'))
        address = parse_address(address)

        phone = validate(detail.xpath('.//div[contains(@class, "property-phone")]')[0].xpath('.//text()')).replace('-', '')
        store_id = validate(detail_request.text.split('var overview_propertyId = "')[1].split('"')[0])

        more_detail_url = "https://www.wyndhamhotels.com/BWSServices/services/search/property/search?propertyId=" + store_id + "&isOverviewNeeded=true&isAmenitiesNeeded=true&channelId=tab&language=en-us"
        detail_request = requests.get(more_detail_url)
        detail = json.loads(detail_request.text)['properties'][0]
        state = validate(detail['stateCode'])
        title = validate(detail['name'])
        latitude = validate(detail['latitude'])
        longitude = validate(detail['longitude'])
        country_code = validate(detail['countryCode'])
        hours = "24 hours open"

        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(address['street']) #address
        output.append(address['city']) #city
        output.append(address['state']) #state
        output.append(address['zipcode']) #zipcode
        output.append(country_code) #country code
        output.append(store_id) #store_number
        output.append(phone) #phone
        output.append("AmericInn hotels") #location type
        output.append(latitude) #latitude
        output.append(longitude) #longitude
        output.append(hours) #opening hours

        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
