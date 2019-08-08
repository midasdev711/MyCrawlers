import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.myowens.com'

def validate(items):
    rets = []
    for item in items:
        
        if item is '<MISSING>':
            continue
        if type(item) is str:
            item = item.encode('ascii','ignore').encode('utf-8').strip()

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
    url = "https://www.myowens.com/wp-admin/admin-ajax.php?action=store_search&lat=40.58654&lng=-122.39168&max_results=25&search_radius=50&autoload=1"
    headers={
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "PHPSESSID=24caa11297ea991306e097308a29c3d0; __utma=143926953.1836670899.1565178648.1565178648.1565178648.1; __utmc=143926953; __utmz=143926953.1565178648.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; mailmunch_second_pageview=true; _mailmunch_visitor_id=21249aea-6e92-4f5d-a154-466d4f635830; _mailmunch_seen_month=true; __utmb=143926953.2.10.1565178648",
        "referer": "https://www.myowens.com/locations/",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
        }
    request = requests.get(url, headers=headers)
    store_list = json.loads(request.text)
    for store in store_list:
        output = []
        hours = store.get('hours')
        store_hours = ""
        hour_infos = hours.split('<tr>')[1:]
        for info in hour_infos:
            hour = info.split('<td>')[1:]
            if '</time>' in hour[1]:
                store_hours += hour[0].split('</td>')[0] + u" " + hour[1].split('<time>').pop().split('</time>')[0] + u","
            else:
                store_hours += hour[0].split('</td>')[0] + u" " + hour[1].split('</td>')[0] + u","
        output.append(base_url)
        output.append(store.get('store'))
        output.append(store.get('address'))
        output.append(store.get('city'))
        output.append(store.get('state'))
        output.append(store.get('zip'))
        output.append('US')
        output.append(store.get('id'))
        output.append(store.get('phone'))
        output.append('hearing centres')
        output.append(store.get('lat'))
        output.append(store.get('lng'))
        output.append(store_hours)
        output_list.append(validate(output))
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
