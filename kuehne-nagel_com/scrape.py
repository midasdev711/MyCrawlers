import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'http://kuehne-nagel.com'

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
    url = "https://www.kn-portal.com/webservice/locations"
    request = requests.get(url)
    regions = json.loads(request.text)
    store_lists = []

    for region in regions:
        if region['region'] == 'North America':
	        for idx, country in region['regionList'][0]['countryList'].items():
	            country_code = country['country_code']
	            if country_code == 'US' or country_code == 'CA':
		            for office in country['officeList']:
		                output = []
		                output.append(base_url)
		                output.append(validate(office['locationName']))
		                output.append(validate(office['buildingNo'] + ' ' + office['street']))
		                output.append(validate(office['city']))
		                output.append(validate(office['stateRegion']))
		                output.append(validate(office['postalCode']))
		                output.append(validate(country_code))
		                output.append(validate(office['cid']))
		                output.append(get_value(office['phoneNumber'].replace('+','').replace('-','')))
		                output.append(validate(office['locationType']))
		                output.append(validate(office['latitude']))
		                output.append(validate(office['longitude']))
		                output.append(get_value(office['openingHours']).replace('\r\n', ' '))
		                output_list.append(output)
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
