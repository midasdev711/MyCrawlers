import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.asics.com'

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
    url = "https://www.locally.com/stores/conversion_data?has_data=true&company_id=1682&store_mode=&style=&color=&upc=&category=&inline=1&show_links_in_list=&parent_domain=&map_center_lat=13.705262631467338&map_center_lng=-99.05341342561687&map_distance_diag=10884.316872931971&sort_by=proximity&no_variants=0&only_retailer_id=&dealers_company_id=&only_store_id=false&uses_alt_coords=false&q=false&zoom_level=1.4783787658592598"
    request = requests.get(url)
    store_list = json.loads(request.text)['markers']
    for store in store_list:
        country = validate(store['country'])
        if country != "US" and country != "CA":
            continue
        hours = ""
        labels = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

        for label in labels:
        	opentime = get_value(str(store.get(label + '_time_open')))
        	if opentime == "0":
        		continue
        	closetime = get_value(str(store.get(label + '_time_close')))
        	if closetime == "0":
        		continue
        	opentime = opentime[:len(opentime) - 2] + ':' + opentime[len(opentime) - 2:]
        	closetime = closetime[:len(closetime) - 2] + ':' + closetime[len(closetime) - 2:]
        	hour = label.title() + ' ' + opentime + '-' + closetime + ' '
        	hours += hour
        
        output = []
        output.append(base_url) # url
        output.append(validate(store['name'])) #location name
        output.append(validate(store['address'])) #address
        output.append(validate(store['city'])) #city
        output.append(validate(store['state'])) #state
        output.append(validate(store['zip'])) #zipcode
        output.append(validate(store['country'])) #country code
        output.append(store["company_id"]) #store_number
        output.append(get_value(store["phone"])) #phone
        output.append("Official ASICS online store") #location type
        output.append(validate(store["lat"])) #latitude
        output.append(validate(store["lng"])) #longitude
        output.append(get_value(hours)) #opening hours

        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
