import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.pompstire.com'

def validate(document):
    rets = []
    for item in document:
        item = item.encode('ascii', 'ignore').encode("utf8").replace(u'\u2019', '').strip()
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
    url = "https://www.pompstire.com/locations.aspx"
    request = requests.get(url)
    response = etree.HTML(request.text.encode("utf-8"))
    store_list = response.xpath('//div[@class="loclisting"]')
    for idx, store in enumerate(store_list):
        output = []
        info = store.xpath('.//div[@class="locationInfo"]')
        hours = store.xpath('.//div[@class="locationhours"]//text()')[2:]
        store_hours = ",".join(hours).replace("\r\n", '').replace("  ", '')[:-2]
        output.append(base_url) #locator_domain
        output.append(" ".join(store.xpath('.//div[@id="info"]//p[@class="subtitle"]//strong/text()'))) #location_name
        output.append("".join(info[0].xpath('.//text()')).split('\r\n')[3].replace('  ', '')[:-1]) #street_address
        output.append("".join(info[0].xpath('.//text()')).split('\r\n')[4].split(",")[0].replace('  ', '')) #city
        output.append("".join(info[0].xpath('.//text()')).split('\r\n')[4].split(",")[1].split(' ')[1]) #state
        output.append("".join(info[0].xpath('.//text()')).split('\r\n')[4].split(",")[1].split(' ').pop()) #zip
        output.append('US') #country_code
        output.append(str(idx + 1)) #store_number
        output.append(store.xpath('.//div[@class="locphone"]/text()').pop().replace('\r\n   ', '').replace('  ', '')) #phone
        output.append("Pomps Tire") #location_type
        output.append("<MISSING>") #latitude
        output.append("<MISSING>") #longitude
        output.append(store_hours) #hours_of_operation
        output = validate(output)

        output_list.append(output)
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
