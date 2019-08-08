import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.hearinglife.ca'

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
    url = "https://www.hearinglife.ca/webservices/centerlocator.svc/GetCenters/%7B6B8D4C17-298F-47DA-82F8-0628E2C8C6C9%7D/null/null/en-ca/"
    headers={
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "ASP.NET_SessionId=znfhse0rdzdnzu5xwqxkdj11; _ga=GA1.2.412036171.1565172381; _gid=GA1.2.293429706.1565172381; _gat_UA-42935243-1=1; _hjid=15667ba2-f38c-491a-8097-356e935c47e1; _hjIncludedInSample=1; _fbp=fb.1.1565172383943.299340127; SC_ANALYTICS_GLOBAL_COOKIE=21b7acba52a948d4af52131f296af25e|True; _gcl_au=1.1.546395052.1565172391; mTrackingPageViewCount=3; mTrackingTimeOnSite=43500",
        "Host": "www.hearinglife.ca",
        "Referer": "https://www.hearinglife.ca/centre-locator",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }
    request = requests.get(url, headers=headers)
    store_list = json.loads(request.text)['Centers']
    for store in store_list:
        output = []
        hours = store.get('OpeningDayHours')
        store_hours = ""
        if len(hours) > 0:
            for x in hours:
                store_hours += (x.get('Day') or u' ') + u' ' + (x.get('OpeningHours') or u' ') + u','
        output.append(base_url)
        output.append(store.get('Title'))
        output.append(store.get('Address'))
        output.append(store.get('City'))
        output.append(store.get('Region'))
        output.append(store.get('PostalCode'))
        output.append('CA')
        output.append(store.get('Id'))
        output.append(store.get('Phonenumber'))
        output.append(store.get('CenterType'))
        output.append(store.get('Latitude'))
        output.append(store.get('Longitude'))
        output.append(store_hours)
        output_list.append(validate(output))
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
