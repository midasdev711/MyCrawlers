import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.hiltongrandvacations.com'

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
    url = "https://www.hiltongrandvacations.com/destinations/"
    request = requests.get(url)
    response = etree.HTML(request.text)
    store_list = response.xpath('//div[contains(@class, "resortpanel")]')
    for store in store_list:
        title = validate(store.xpath("./@data-name"))
        city = validate(store.xpath("./@data-city"))
        loc_info = validate(store.xpath(".//p[@class='location']//text()")).split(', ')
        country = loc_info.pop()
        state = loc_info.pop()

        detail_url = validate(store.xpath(".//p[@class='more']/a/@href"))
        detail_request = requests.get(detail_url)
        detail = etree.HTML(detail_request.text)

        hours_phone = get_value(eliminate_space(detail.xpath(".//div[@id='info']//text()")))
        if "Coming Soon" in hours_phone:
            continue
        hours = ""
        if "Check" not in hours_phone:
            hours = "<MISSING>"
        else:
            hours_phone = re.sub("(\w+) (\w+): (\w+) (\w+).(\w+).", r'<hours>\1 \2: \3 \4.\5.<hours>', hours_phone)
            hours_tmp = hours_phone.split("<hours>")
            for hour in hours_tmp:
                if "Check " in hour:
                    hours += hour + ' '

        if "Phone" not in hours_phone:
            phone = "<MISSING>"
        else:
            regex_str = []
            regex = r"(\d{3}-\d{3}-\d{4})|(\+\d{2} \d{4} \d{6})|(\+\d{2} \d{3} \d{3} \d{4})|(\+\d{2} \d{2} \d{2} \d{2} \d{4})"
            phone = re.findall(regex, hours_phone)
            if len(phone) > 0:
                phone = phone[0]
                phone = eliminate_space(phone)
                if len(phone) == 0:
                    phone = '<MISSING>'
                else:
                    phone = phone.pop(0)
            else:
                phone = '<MISSING>'
            

        geoinfo = detail_request.text.split('new google.maps.LatLng(')[1].split(')')[0]

        output = []
        output.append(base_url) # url
        output.append(title) #location name
        output.append("<MISSING>") #address
        output.append(city) #city
        output.append(state) #state
        output.append("<MISSING>") #zipcode
        output.append(country) #country code
        output.append("<MISSING>") #store_number
        output.append(phone) #phone
        output.append("Hilton Grand Vacations Resort") #location type
        output.append(geoinfo.split(', ')[0]) #latitude
        output.append(geoinfo.split(', ')[1]) #longitude
        output.append(hours) #opening hours

        output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
