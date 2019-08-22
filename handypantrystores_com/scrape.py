import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.handypantrystores.com'

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
    url = "https://www.handypantrystores.com/locations"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "_ga=GA1.2.1165629933.1566414107; _gid=GA1.2.1247706018.1566414107; dm_timezone_offset=240; dm_last_page_view=1566414106901; dm_last_visit=1566414106901; dm_total_visits=1; __utma=147943726.1165629933.1566414107.1566414109.1566414109.1; __utmc=147943726; __utmz=147943726.1566414109.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=147943726.1f5cc183; __utmt_b=1; __utmt_c=1; _gat=1; dm_this_page_view=1566414317426; __utmb=147943726.8.10.1566414109; _sp_id.0ec6=ade1b2784c6ee4c9.1566414109.1.1566414318.1566414109; _sp_ses.0ec6=1566416117710",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    request = requests.get(url, headers=headers)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[@class="dmContent"]//div[@class="dmRespColsWrapper"]//div[contains(@class,"dmRespCol")]')
    store_list.pop()
    store_list.pop(0)
    for store in store_list:
        geoinfo = store.xpath(".//div[@data-type='inlineMap']")[0]

        address = get_value(geoinfo.xpath('./@data-address'))

        output = []
        output.append(base_url) # url
        output.append(get_value(store.xpath(".//div[contains(@class, 'dmNewParagraph')]//text()")[0])) #location name
        output.append(address.split(",")[0]) #address
        output.append(address.split(",")[1]) #city
        output.append(address.split(",")[2]) #state
        output.append("<MISSING>") #zipcode
        output.append(get_value(geoinfo.xpath('./@country'))) #country code
        output.append("<MISSING>") #store_number
        output.append(get_value(store.xpath('.//a[contains(@class, "voipReplacement")]/@phone'))) #phone
        output.append("HANDY PANTRY-Friendly Food Stores") #location type
        output.append(get_value(geoinfo.xpath('./@data-lat'))) #latitude
        output.append(get_value(geoinfo.xpath('./@data-lng'))) #longitude
        output.append(get_value(store.xpath('.//dl[@class="open-hours-data"]//text()')).replace('\n', '')) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
