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

def toggle_quote(source):
    res = []
    for x in source:
        tmp = ""
        if x == "'":
            tmp = '"'
        elif x == '"':
            tmp = "'"
        else:
            tmp = x
        res.append(tmp)
    return "".join(res)

def fetch_data():
    output_list = []
    url = "https://prairielife.com/locations/"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[@class="location"]')

    geoinfo_tmp = toggle_quote(list(validate(request.text.split('features = ')[1].split('features.forEach')[0][:-21])))
    geoinfo_tmp = re.sub("(\w) (\w)", r'\1 \2', geoinfo_tmp)
    geoinfo_tmp = json.loads(re.sub("(\w+):", r'"\1":',  geoinfo_tmp).encode('utf8'))
    geoinfo = {}
    for x in geoinfo_tmp:
        geoinfo[validate(x['title'])] = {"lat": x['position']['lat'], "lng": x['position']['lng']}

    for store in store_list:
        detail_url = store.xpath(".//a[@class='btn-locations']/@href")[0]
        detail_request = requests.get(base_url + detail_url[2:])
        detail = etree.HTML(detail_request.text)

        title = get_value(store.xpath(".//h3//text()"))
        info = eliminate_space(store.xpath('./text()'))

        hour_info = detail.xpath("//div[@class='column B']/div[contains(@class, 'x-long')]")
        labels = eliminate_space(hour_info[1].xpath('./div')[0].xpath('.//text()'))
        hours = eliminate_space(hour_info[1].xpath('./div')[1].xpath('.//text()'))
        store_hours = ""
        for x in xrange(0, len(labels)):
            store_hours += labels[x] + hours[x] + ' '
            
        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append(info[0]) #address
        output.append(info[1].split(', ')[0]) #city
        output.append(info[1].split(', ')[1].split(' ')[0]) #state
        output.append(info[1].split(', ')[1].split(' ')[1]) #zipcode
        output.append('US') #country code
        output.append("<MISSING>") #store_number
        output.append(info[2]) #phone
        output.append("PrairieLife FITNESS - Premium GYM") #location type
        output.append(geoinfo[title]['lat']) #latitude
        output.append(geoinfo[title]['lng']) #longitude
        output.append(store_hours) #opening hours
        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
