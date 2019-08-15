import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.moesoriginalbbq.com/'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').encode("utf8").strip()

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
    url = "https://api.storepoint.co/v1/159d567264b9aa/locations?rq"
    request = requests.get(url)
    store_list = json.loads(request.text)['results']['locations']
    for store in store_list:
        output = []
        address = store.get('streetaddress')
        street_address = address.split(',')[0]
        city = address.split(',')[1]
        try:
            if len(address.split(',')) == 2:
                street_address = address.split(',')[0].split('.')[0]
                city = address.split(',')[0].split('.')[1]
                state = address.split(',')[2].split(' ')[1]
                zipcode = address.split(',')[-1:][0].split(' ')[2]
            elif len(address.split(',')) == 3:
                street_address = address.split(',')[0]
                city = address.split(',')[1]
                state = address.split(',')[2].split(' ')[1]
                zipcode = address.split(',')[-1:][0].split(' ')[2]
            else:
                street_address = address.split(',')[0]
                city = address.split(',')[1]
                state = address.split(',')[2]
                zipcode = address.split(',')[3]
        except:
            pdb.set_trace()
        website = store.get('website')
        detail = requests.get(website)
        try: 
            phone = detail.text.split('Phone:')[1].split('</p>')[0].replace('<strong>', '').replace('</strong>', '').replace('&nbsp;', '')
        except:
            pass
        store_hours = ""
        # try:
        #     store_hours = detail.text.split('<strong>')[5].split('</h2>')[0].replace('</strong>', '').replace('<br/>', ' ')
        # except Exception as e:
        #     if (len(detail.text.split('<h2 class="text-align-right">')) > 1):
        #         store_hours = detail.text.split('<h2 class="text-align-right">')[1].split('</h2>')[0].replace('</strong>', '').replace('<strong>', '').replace('<br/>', ' ')
        #     else:
        #         pdb.set_trace()
        #         # store_hours = detail.text.split('<strong>')[4].split('</h2>')[0].replace('</strong>', '').replace('<br/>', ' ')

        output.append(base_url) #locator_domain
        output.append(store.get('name')) #location_name
        output.append(street_address) #street_address
        output.append(city) #city
        output.append(state) #state
        output.append(zipcode) #zip
        output.append('US') #country_code
        output.append(store.get('id')) #store_number
        output.append(validate(phone)) #phone
        output.append("Moe's Original Bar B Que") #location_type
        output.append(store.get('loc_lat')) #latitude
        output.append(store.get('loc_long')) #longitude
        output.append(store_hours) #hours_of_operation

        output_list.append(output)
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
