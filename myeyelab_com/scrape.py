import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.myeyelab.com/'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.replace(u'\u2013', '-').encode('ascii', 'ignore').encode("utf8").strip()

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
    url = "https://www.myeyelab.com/wp-admin/admin-ajax.php"
    headers={
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-length": "76",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "gclid=undefined; _gcl_au=1.1.1714849535.1565178085; PHPSESSID=d79926914aa9b70057222f442a5d25ae; _ga=GA1.2.1708386539.1565178087; _gid=GA1.2.1227588014.1565178087; _gat_UA-38131623-1=1; _fbp=fb.1.1565178090134.1982884566; _hjid=36bbe2f5-8623-44cf-a5e6-bc30772308de; _hjIncludedInSample=1; __zlcmid=tfiRaC8OCsLC33",
        "origin": "https://www.myeyelab.com",
        "referer": "https://www.myeyelab.com/locations/",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
        }
    form_data = {
        "action": "somel_geo_store_list",
        "nonce": "89823bf4f9"
    }
    request = requests.post(url, headers=headers, data=form_data)
    store_list = json.loads(request.text)['data']['stores']
    for store in store_list:
        output = []
        hours = etree.HTML(store['sl_hours']).xpath('.//text()')

        output.append(base_url)
        output.append(validate(store['sl_web_name']))
        output.append(validate(store['sl_address']))
        output.append(validate(store['sl_city']))
        output.append(validate(store['sl_state']))
        output.append(validate(store['sl_zip']))
        output.append(validate(store['sl_country']))
        output.append(validate(store['sl_id']))
        output.append(validate(store['sl_phone']))
        output.append("My Eyelab - The Optical Retail Industry")
        output.append(validate(store['sl_latitude']))
        output.append(validate(store['sl_longitude']))
        output.append(get_value(hours))
        output_list.append(output)
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
