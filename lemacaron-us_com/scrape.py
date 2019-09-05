import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'https://lemacaron-us.com'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').encode("utf8").strip().replace('\n', '')

def get_value(item):
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
    url = "https://lemacaron-us.com/locations"
    response = requests.get(url)
    store_list = json.loads(response.text.split('var locations = ')[1].split('</script>')[0][:-3])
    for store in store_list:
        output = []
        output.append(base_url) # url
        output.append(validate(store["fran_location_name"])) #location name
        output.append(validate(store["fran_address"])) #address
        output.append(validate(store["fran_city"])) #city
        output.append(validate(store["fran_state"])) #state
        output.append(validate(store["fran_zip"])) #zipcode
        output.append(validate(store["fran_country"])) #country code
        output.append(validate(store["id"])) #store_number
        output.append(validate(store["fran_phone"])) #phone
        output.append("French Macaron Bakery, French Pastry Shop") #location type
        output.append(validate(store["latitude"])) #latitude
        output.append(validate(store["longitude"])) #longitude
        output.append(get_value(store["fran_hours"]).replace('<br>', ' ').replace('\r', '').replace('<br />', ' ').replace('<p>', '').replace('</p>', '')) #opening hours
        if "COMING SOON" in store["name"] or store["fran_phone"] == "Coming Soon" or store["fran_address"] == "Coming Soon":
            continue

        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
