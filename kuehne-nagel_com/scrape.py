import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'http://kuehne-nagel.com'

def validate(items):
    rets = []
    for item in items:
        
        item = item.encode('utf-8').replace('\xe2\x80\x93', '-').strip()
        if item == '':
            item = '<MISSING>'
        if item != '':
            rets.append(item)
    return rets

def write_output(data):
    with open('data.csv', mode='w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["locator_domain", "location_name", "street_address", "city", "state", "zip", "country_code", "store_number", "phone", "location_type", "latitude", "longitude", "hours_of_operation"])
        for row in data:
            writer.writerow(row)
    return

def fetch_data():
    output_list = []
    url = "https://www.kn-portal.com/webservice/locations"
    request = requests.get(url)
    regions = json.loads(request.text)
    store_lists = []

    for region in regions:
        try:
            for country in region.get('regionList')[0].get('countryList'):
                country_code = country.get('country_code')
                for office in country.get('officeList'):
                    output = []
                    # pdb.set_trace()
                    output.append(base_url)
                    output.append(office.get('locationName'))
                    output.append(office.get('buildingNo') + u' ' + office.get('street'))
                    output.append(office.get('city'))
                    output.append(office.get('stateRegion'))
                    output.append(office.get('postalCode'))
                    output.append(country_code)
                    output.append(office.get('cid'))
                    output.append(office.get('phoneNumber').replace('+','').replace(' ','-'))
                    output.append(office.get('locationType'))
                    output.append(office.get('latitude'))
                    output.append(office.get('longitude'))
                    output.append(office.get('openingHours'))
                    # pdb.set_trace()
                    output_list.append(validate(output))
        except:
            keys = list(region.get('regionList')[0].get('countryList').keys())
            for key in keys:
                country = region.get('regionList')[0].get('countryList').get(key)

                country_code = country.get('country_code')
                for office in country.get('officeList'):
                    output = []
                    # pdb.set_trace()
                    output.append(base_url)
                    output.append(office.get('locationName'))
                    output.append(office.get('buildingNo') + u' ' + office.get('street'))
                    output.append(office.get('city'))
                    output.append(office.get('stateRegion'))
                    output.append(office.get('postalCode'))
                    output.append(country_code)
                    output.append(office.get('cid'))
                    output.append(office.get('phoneNumber').replace('+','').replace(' ','-'))
                    output.append(office.get('locationType'))
                    output.append(office.get('latitude'))
                    output.append(office.get('longitude'))
                    output.append(office.get('openingHours'))
                    # pdb.set_trace()
                    output_list.append(validate(output))
        
                # pdb.set_trace()
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
