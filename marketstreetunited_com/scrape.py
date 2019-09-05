import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'https://www.marketstreetunited.com'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').encode("utf8").strip().replace('\n', '')

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
    url = "https://www.marketstreetunited.com/Sysnify.Relationshop.v2/StoreLocation/SearchStore?__RequestVerificationToken=euPudG87EY_RqGcvZOq1c5YJkWkCDyQFs0jo4DZBA8p6EG-7lSCtr1kZDndiv7LEI-rBU3A6S9WsnvfuryBXvlkNks85izIa4cne7GA_5nw1&zipcode=&cityStore=&banner=false&isDelivery=false&isPickup=false&_=1565870079052"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "_gcl_au=1.1.1235651713.1565818178; _ga=GA1.2.890403004.1565818181; _gid=GA1.2.282974722.1565818181; _fbp=fb.1.1565818183410.190159251; hubspotutk=8bca51f6370b3b8ceb7860a3b934c931; COOKIE_CURRENT_PAGE=%2frs%2fWeeklyAd; COOKIE_IS_PRIVATE=False; showhideMenuData=1,1,1; __RequestVerificationToken=4NjnTYnBz3CjKes_oD0sKDF8c_OAbLPhH_OuMA4j9n0kvUFWSkrn_weHJYS0xYktdCen2j9CblObdfeHZNY0-IeNA_ZZ9MYENIj031tFjXE1; ASP.NET_SessionId=exh1ly3z4ucwsibxwfrmvpgz; __hstc=17894758.8bca51f6370b3b8ceb7860a3b934c931.1565818184323.1565818184323.1565870001804.2; __hssrc=1; __hssc=17894758.3.1565870001804",
        "Host": "www.marketstreetunited.com",
        "Referer": "https://www.marketstreetunited.com/rs/StoreLocator",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.get(url, headers=headers)
    store_list = json.loads(response.text.split('var stores = ')[1].split('var ')[0][:-11])
    for store in store_list:
        output = []
        output.append(base_url) # url
        output.append(validate(store["StoreName"])) #location name
        output.append(validate(store["Address1"])) #address
        output.append(validate(store["City"])) #city
        output.append(validate(store["State"])) #state
        output.append(validate(store["Zipcode"])) #zipcode
        output.append('US') #country code
        output.append(store["StoreID"]) #store_number
        output.append(validate(store["PhoneNumber"])) #phone
        output.append("Market Street in US") #location type
        output.append(validate(str(store["Latitude"]))) #latitude
        output.append(validate(str(store["Longitude"]))) #longitude
        output.append(get_value(store["StoreHours"])) #opening hours
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
