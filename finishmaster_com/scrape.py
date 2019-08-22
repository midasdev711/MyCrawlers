import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'http://www.finishmaster.com'

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
    url = "http://www.finishmaster.com/includes/locations.php"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "X-Mapping-mmgahdea=41E3717323B9668EB33FEABDCA7BD186; _ga=GA1.2.1524943330.1566503329; _gid=GA1.2.1513815211.1566503329; _gat=1; D_IID=C892E37C-A3E9-357E-8B59-7A03CF4E645E; D_UID=13A8ED66-9797-3D6C-836D-385863436C56; D_ZID=B12DC2A2-30F1-3F40-9766-A081B29F0B7C; D_ZUID=411EBF52-223F-31C6-A222-3808AA0F8526; D_HID=E4131794-0874-3B2D-A7C4-3EC9038869D0; D_SID=104.200.132.222:0Qk/q6NFvVnMhVbG2zs22tjL9PO2L4BuepRhm5WApLQ",
        "Host": "www.finishmaster.com",
        "Referer": "http://www.finishmaster.com/locations/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "X-Distil-Ajax": "raurasvecwaraqzwrdebevrerszfsd",
        "X-Requested-With": "XMLHttpRequest"
    }
    request = requests.get(url, headers=headers)
    store_list = json.loads(request.text.encode("utf8"))['marker']
    for store in store_list:
        store = store['@attributes']
        citystatezip = validate(store['citystatezip'])

        output = []
        output.append(base_url) # url
        output.append(validate(store['title'])) #location name
        output.append(validate(store['street'])) #address
        output.append(citystatezip.split(', ')[0]) #city
        output.append(citystatezip.split(', ')[1].split(' ')[0]) #state
        output.append(citystatezip.split(', ')[1].split(' ')[1]) #zipcode
        output.append('US') #country code
        output.append('<MISSING>') #store_number
        output.append(validate(store['telephone'])) #phone
        output.append("FinishMaster | Automotive and Industrial Paint Refinishing Leaders") #location type
        output.append(validate(store['lat'])) #latitude
        output.append(validate(store['lng'])) #longitude
        output.append(validate(store['hours'])) #opening hours

        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
