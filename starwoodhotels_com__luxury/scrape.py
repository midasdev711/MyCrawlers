import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://the-luxury-collection.marriott.com'

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
    url = "https://the-luxury-collection.marriott.com/hotel-directory/"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "AMCVS_664516D751E565010A490D4C%40AdobeOrg=1; s_ecid=MCMID%7C12727990337978408002082029743296042069; AMCV_664516D751E565010A490D4C%40AdobeOrg=-330454231%7CMCIDTS%7C18143%7CMCMID%7C12727990337978408002082029743296042069%7CMCAAMLH-1568106461%7C9%7CMCAAMB-1568106461%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1567508861s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2; mt.v=2.852703313.1567501667631; s_cc=true; mt.pc=2.1; AAMC_marriottinternationa_0=REGION%7C9; aam_uuid=12833842366109618652054283367276747324; mt.g.83432638=2.852703313.1567501667631; _fbp=fb.1.1567501675373.1372649452; adcloud={%22_les_v%22:%22y%2Cmarriott.com%2C1567503896%22}; s_sq=%5B%5BB%5D%5D",
        "referer": "https://the-luxury-collection.marriott.com/",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
    }
    request = requests.get(url, headers=headers)
    location_text = request.text.split('MARRIOTT_GEO_DATA = ')[1].split('</script>')[0][:-4]
    store_list = json.loads(location_text)['properties']
    for idx, store in store_list.items():
        if validate(store['country']) != 'US':
            continue
        city = validate(store['city'].split('_')[:-3]).title()
        output = []
        output.append(base_url) # url
        output.append(validate(store['name'])) #location name
        output.append(validate(store['address'])) #address
        output.append(city) #city
        output.append(validate(store['state'])) #state
        output.append(validate(store['zipcode'])) #zipcode
        output.append("US") #country code
        output.append(validate(idx)) #store_number
        output.append(validate(store['phone'])) #phone
        output.append("Luxury Hotels & Resorts | The Luxury Collection") #location type
        output.append(validate(store['latitude'])) #latitude
        output.append(validate(store['longitude'])) #longitude
        output.append("<MISSING>") #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
