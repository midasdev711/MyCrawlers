import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://prairielife.com'

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
    url = "https://www.happyspizza.com/wp-admin/admin-ajax.php"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "2387",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "__cfduid=df92c4dcc7b2c70822a7a87be163eab451566555836; _ga=GA1.2.1745778772.1566555845; _gid=GA1.2.1412165309.1566555845; g1_preheader_open_on_startup=false; _gat=1",
        "Host": "www.happyspizza.com",
        "Origin": "https://www.happyspizza.com",
        "Referer": "https://www.happyspizza.com/store-locator/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    form_data = {
        "formdata": "nameSearch=&addressInput=&addressInputCity=&addressInputState=&addressInputCountry=&ignore_radius=0",
        "action": "csl_ajax_onload",
    }
    request = requests.post(url, headers=headers, data=form_data)
    store_list = json.loads(request.text)['response']
    
    for store in store_list:
        detail_url = etree.HTML(store['web_link']).xpath('.//a/@href')[0]
        detail_request = requests.get(detail_url)
        detail = get_value(eliminate_space(etree.HTML(detail_request.text).xpath('.//text()')))
        store_hours = detail.split('Store Hours: ')[1].split(' Order Online')[0]
        
        output = []
        output.append(base_url) # url
        output.append(validate(store['name'])) #location name
        output.append(validate(store['address2'])) #address
        output.append(validate(store['city'])) #city
        output.append(validate(store['state'])) #state
        output.append(validate(store['zip'])) #zipcode
        output.append('US') #country code
        output.append(validate(store['id'])) #store_number
        output.append(validate(store['phone'])) #phone
        output.append("Happy's Pizza | Hand Tossed Pizza") #location type
        output.append(validate(store['lat'])) #latitude
        output.append(validate(store['lng'])) #longitude
        output.append(store_hours) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
