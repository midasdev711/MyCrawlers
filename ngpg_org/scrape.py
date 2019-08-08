import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.ngpg.org'

def write_output(data):
    with open('data.csv', mode='w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["locator_domain", "location_name", "street_address", "city", "state", "zip", "country_code", "store_number", "phone", "location_type", "latitude", "longitude", "hours_of_operation"])
        for row in data:
            writer.writerow(row)
    return

def fetch_data():
    output_list = []
    url = "https://www.ngpg.org/fm/index/practice-map-data"
    headers={
        "Accept": "application/xml, text/xml, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "PHPSESSID=n61uqj715ge4tdt4ftn2eupm61; calltrk_referrer=direct; calltrk_landing=https%3A//www.ngpg.org/; calltrk_session_id=1cec532f-1a2c-46d5-b794-1552cde2aaad; _ga=GA1.2.960686148.1565205054; _gid=GA1.2.142616363.1565205054; calltrk_fcid=f761d4f7-7d8c-4800-8f6b-9fc13f88ba2c; crFormCapture=form%255Bbh_sl_address%255D%3D30597%26metadata%255Bbh_sl_address%255D%3Da%26metadata%255Bcategory%255D%3Da%26form_metadata%255Bid%255D%3Dbh-sl-user-location%26form_metadata%255Bmethod%255D%3Dget%26form_metadata%255Baction%255D%3D%252Fpractice-map%252F%26session_uuid%3D1cec532f-1a2c-46d5-b794-1552cde2aaad%26fcid%3Df761d4f7-7d8c-4800-8f6b-9fc13f88ba2c%26uuid%3Dac30ad4b-fa5c-4748-b2b2-1540b1d39de8%26timestamp%3D1565205605240%26url%3Dhttps%253A%252F%252Fwww.ngpg.org%252Fpractice-map%252F%26landing%3Dhttps%253A%252F%252Fwww.ngpg.org%252F%26referrer_url%3Ddirect%26referrer%3Ddirect; _gali=bh-sl-address",
        "Host": "www.ngpg.org",
        "Referer": "https://www.ngpg.org/practice-map/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }
    request = requests.get(url, headers=headers)
    response = etree.HTML(request.text.encode("utf-8"))
    store_list = response.xpath('//marker')
    for store in store_list:
        output = []
        detailurl = store.xpath('./@web')[0]
        detailrequest = requests.get('https://www.ngpg.org' + detailurl)
        detailresponse = etree.HTML(detailrequest.text.encode("utf-8"))
        details = detailresponse.xpath('//div[contains(@class, "cleft-subleft")]//text()')
        details = ''.join(details).split('Hours:').pop().strip().replace('\r\n', '')
        store_hours = details.encode("utf-8").replace('\xe2\x80\x93', '').replace('\xc2\xa0', '').split('Insurance:')[0]
        if 'p.m' not in store_hours:
            store_hours = "<MISSING>"
        if not store_hours.endswith('p.m.'):
            store_hours = store_hours.split('Get general information')[0].split("Saturday morning injury clinics")[0].split('This clinic ')[0]
        zipcode = store.xpath('./@postal')[0]
        if zipcode == None or zipcode == "":
            zipcode = "<MISSING>"
        phone = store.xpath('./@phone')[0].replace('\r\n', '')
        if phone == "" or phone == None:
            phone = "<MISSING>"
        output.append(base_url)
        output.append(store.xpath('./@name')[0])
        output.append(store.xpath('./@address')[0])
        output.append(store.xpath('./@city')[0])
        output.append(store.xpath('./@state')[0])
        output.append(zipcode)
        output.append('US')
        output.append('PHYSICIANS GROUP')
        output.append(phone)
        output.append(store.xpath('./@category')[0])
        output.append(store.xpath('./@lat')[0])
        output.append(store.xpath('./@lng')[0])
        output.append(store_hours)
        output_list.append(output)
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
