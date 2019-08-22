import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.globoshoes.com'

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
    url = "https://www.globoshoes.com/api/stores?allStores=true&countryCode=ca&lat=56.130366&lng=-106.34677099999999"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "cookie": "x-aldo-api-version=2; sessionId=3b33e872-437a-4c37-9e6f-b706fcb688ba; optimizelyEndUserId=oeu1566463778219r0.49132819238438064; _gcl_au=1.1.1726986112.1566463778; _ga=GA1.2.1133986485.1566463778; _gid=GA1.2.694498855.1566463778; _gat_UA-49129446-15=1; _dc_gtm_UA-49129446-7=1; stc117157=tsa:1566463781051.1841856223.2944946.5944867539654857.:20190822091941|env:1%7C20190922084941%7C20190822091941%7C1%7C1066662:20200821084941|uid:1566463781051.702941445.786161.117157.1316350382.2:20200821084941|srchist:1066662%3A1%3A20190922084941:20200821084941; _fbp=fb.1.1566463781705.1774835318; lastRskxRun=1566463784147; rskxRunCookie=0; rCookie=lbwp6b5lkpr5rxyfif9mbjzmg3bh2; cto_lwid=854b1787-2eb4-45bc-8204-64e16eb0b583; ROUTEID=.node33; _gat_UA-49129446-7=1; regionCode=ca; languageCode=en; ADRUM_BT=R:0|g:6f5c524c-5ae1-4ead-98d8-5e2d5e9b03fd16492|n:aldo_689ee717-e80b-4b94-9833-5714a40e5d2e",
        "referer": "https://www.globoshoes.com/",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "x-aldo-api-version": "2",
        "x-aldo-brand": "globoshoes",
        "x-aldo-lang": "en",
        "x-aldo-region": "ca",
    }
    request = requests.get(url, headers=headers)
    store_list = json.loads(request.text)['stores']
        
    for store in store_list:
        hours = store['openingHours']['weekDayOpeningList']
        store_hours = ""

        for hour in hours:
            store_hours += hour['weekDay']
            if hour['closed'] == True:
                store_hours += ': Closed '
            else:
                store_hours += ': ' + hour['openingTime']['formattedHour'] + '-' + hour['closingTime']['formattedHour'] + ' '
        formattedAddress = store['address']['formattedAddress']

        title = 'Globo at ' + validate(store['address']['line1'])
        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(validate(store['address']['line1'])) #address
        output.append(validate(formattedAddress.split(', ')[-2:][0])) #city
        output.append(validate(formattedAddress.split(', ')[-3:][0])) #state
        output.append(validate(store['address']['postalCode'])) #zipcode
        output.append('CA') #country code
        output.append(store['name']) #store_number
        output.append(validate(store['address']['phone'])) #phone
        output.append("Globo Shop Canada") #location type
        output.append(store['geoPoint']['latitude']) #latitude
        output.append(store['geoPoint']['longitude']) #longitude
        output.append(validate(store_hours)) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
