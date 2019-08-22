import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://eatatthegarage.com'

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
    url = "https://eatatthegarage.com/locations/"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "__cfduid=d01034d7a23e455a5ecaf7416a80910621566482991; _ga=GA1.2.188225528.1566482993; _gid=GA1.2.1580815073.1566482993; _fbp=fb.1.1566482994404.1500101159",
        "referer": "https://eatatthegarage.com/",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    request = requests.get(url, headers=headers)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[contains(@class, "location-card")]')

    geoinfo_tmp = json.loads(request.text.split('var guteLocations = ')[1].split('</script>')[0])
    geoinfo = {}
    for x in geoinfo_tmp:
        title = validate(x['title'])
        geoinfo[title] = {"lat": x['lat'], "long": x['long']}
        
    for store in store_list:
        detail_url = validate(store.xpath(".//h2[@class='title']//a/@href"))
        detail_request = requests.get(detail_url, headers=headers)
        detail = etree.HTML(detail_request.text)

        title = validate(store.xpath(".//h2[@class='title']//text()"))
        info = validate(store.xpath(".//address//text()")).split(', ')
        if not geoinfo.get(title):
            geoinfo[title] = {"lat": "<MISSING>", "long": "<MISSING>"}

        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(info[0]) #address
        output.append(info[1]) #city
        output.append(info[2].split(' ')[0]) #state
        output.append(info[2].split(' ')[1]) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append(validate(store.xpath('.//div[contains(@class, "location-listing-info")]/p//text()'))) #phone
        output.append("The Garage | Get the Finest Burgers and Hamburgers in Town") #location type
        output.append(geoinfo[title]['lat']) #latitude
        output.append(geoinfo[title]['long']) #longitude
        output.append(get_value(eliminate_space(detail.xpath(".//p[@class='hours']//text()"))).replace('\n', '')) #opening hours

        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
