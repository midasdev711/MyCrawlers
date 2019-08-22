import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'https://lamadeleine.com'

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
    url = "https://cms.lamadeleine.com/wp-json/wp/v2/restaurant-locations?per_page=150"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://lamadeleine.com/locations",
        "Sec-Fetch-Mode": "cors",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    store_list = json.loads(response.text)
    for store in store_list:
        hours = store["acf"]["locationHero"]["hoursOfOperation"]
        store_hours = ""
        for x in hours:
            if x['openingTime'] == "Closed":
                store_hours += x['day'] + ": Closed "
            else:
                store_hours += x['day'] + ":" + x['openingTime'] + '-' + x['closingTime'] + ' '
        output = []
        output.append(base_url) # url
        output.append(validate(store["acf"]["locationHero"]["storeName"])) #location name
        output.append(validate(store["acf"]["locationHero"]["addressLine1"])) #address
        output.append(validate(store["acf"]["locationHero"]["city"])) #city
        output.append(validate(store["acf"]["locationHero"]["state"])) #state
        output.append(validate(store["acf"]["locationHero"]["zip"])) #zipcode
        output.append('US') #country code
        output.append(validate(store["acf"]["locationHero"]["id"])) #store_number
        output.append(validate(store["acf"]["locationHero"]["phone"])) #phone
        output.append("LA MADELEINE restauraunt") #location type
        output.append(validate(store["acf"]["locationHero"]["lat"])) #latitude
        output.append(validate(store["acf"]["locationHero"]["lng"])) #longitude
        output.append(get_value(store_hours)) #opening hours
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
