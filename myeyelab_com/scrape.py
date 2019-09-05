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
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "PHPSESSID=9498d8c3f310d131eb6f18b4f375428f; gclid=undefined; _gcl_au=1.1.270807480.1567276928; _ga=GA1.2.1245547417.1567276928; _gid=GA1.2.732769914.1567276928; _hjid=627595e1-43fa-472e-b8ea-8810f6c343a6; _hjIncludedInSample=1; _fbp=fb.1.1567276929766.1440445499; __zlcmid=u3iVHICLo1D5sL; _gat_UA-38131623-1=1",
        }
    form_data = {
        "action": "somel_geo_store_list",
        "nonce": "4da222d7a9"
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
