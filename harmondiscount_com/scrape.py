import csv
import re
import pdb
import requests
from lxml import etree
import json

base_url = 'https://www.harmondiscount.com'

def validate(items):
    rets = []
    for item in items:
        if item is '<MISSING>':
            continue
        if type(item) != str:
            item = str(item)
        item = item.encode('utf-8').strip()
        if item != '':
            rets.append(str(item))
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
    url = "https://www.harmondiscount.com/api/commerce/storefront/locationUsageTypes/SP/locations/?pageSize=268&includeAttributeDefinition=true"
    headers={
        "path": "/api/commerce/storefront/locationUsageTypes/SP/locations/?pageSize=268&includeAttributeDefinition=true",
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
        'cookie': 'sb-sf-at-prod-s=pt=&at=FHdMO91ME7TK1Wiqjgs2z9KCrtwo2c7Vaqga0ciWdlMH/yYxOek17l+briGEbfVDWUN5NvTlB+0UgQqWFLN3np4oqso/980gEm2MUKUpmCWCJPOWLtbUwbCOgf+tZXXzkCC38wRHpUiaoHoyl6CXOpbeADT70u8/fW2mycWX1q6b3mISale/tJOW9hZrnnB4FSf5R4QReD/nApWK/MGz50fJCvz5O/OwfULpWAW1mmBPpV8chy/WOmk0ssdC4FS/WI+Qi47TKnVLZI8iCVcCd7zyR/nKVgxabEIlnq4QGuNcTwZTQmhwz0AaikwtzYN/WsM+LhdBwfLbnJgBoUqdqQ==&dt=2019-08-07T08:52:21.5022633Z; sb-sf-at-prod=pt=&at=FHdMO91ME7TK1Wiqjgs2z9KCrtwo2c7Vaqga0ciWdlMH/yYxOek17l+briGEbfVDWUN5NvTlB+0UgQqWFLN3np4oqso/980gEm2MUKUpmCWCJPOWLtbUwbCOgf+tZXXzkCC38wRHpUiaoHoyl6CXOpbeADT70u8/fW2mycWX1q6b3mISale/tJOW9hZrnnB4FSf5R4QReD/nApWK/MGz50fJCvz5O/OwfULpWAW1mmBPpV8chy/WOmk0ssdC4FS/WI+Qi47TKnVLZI8iCVcCd7zyR/nKVgxabEIlnq4QGuNcTwZTQmhwz0AaikwtzYN/WsM+LhdBwfLbnJgBoUqdqQ==; _mzvr=safJ6OXT9kuulpJAms_jmw; _mzvs=nn; _mzvt=ZFFLjm_iBkywI1hjDujwEw; BVImplmain_site=12305; rkglsid=h-aa9bd91c85aae663735afa7816c6b478_t-1565167944; __utma=41580219.178870931.1565167948.1565167948.1565167948.1; __utmc=41580219; __utmz=41580219.1565167948.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); BVBRANDID=732f4313-05f4-4de2-a8b2-b92dad5d3774; BVBRANDSID=b216d335-e27d-43b6-9b1f-e4f15739a0ba; mozucart=%7B%22itemCount%22%3A0%2C%22totalQuantity%22%3A0%2C%22total%22%3A0%2C%22isExpired%22%3Afalse%2C%22hasActiveCart%22%3Atrue%7D; _fbp=fb.1.1565167948308.420085402; popupEnabled=1; bn_u=6927905453064564722; __utmt=1; __utmb=41580219.6.10.1565167948; _mzPc=eyJjb3JyZWxhdGlvbklkIjoiMzlkYjAxYzVkYTA4NDdjNThhYjU5NDg5MTg2YzFiZWYiLCJpcEFkZHJlc3MiOiIxODUuMTUzLjE3OS4zMSIsImlzRGVidWdNb2RlIjpmYWxzZSwiaXNDcmF3bGVyIjpmYWxzZSwiaXNNb2JpbGUiOmZhbHNlLCJpc1RhYmxldCI6ZmFsc2UsImlzRGVza3RvcCI6dHJ1ZSwidmlzaXQiOnsidmlzaXRJZCI6IlpGRkxqbV9pQmt5d0kxaGpEdWp3RXciLCJ2aXNpdG9ySWQiOiJzYWZKNk9YVDlrdXVscEpBbXNfam13IiwiaXNUcmFja2VkIjpmYWxzZSwiaXNVc2VyVHJhY2tlZCI6ZmFsc2V9LCJ1c2VyIjp7ImlzQXV0aGVudGljYXRlZCI6ZmFsc2UsInVzZXJJZCI6ImRlNDQyZmZmMGI1YjRmZDViOWZlMGQ1ZmI1YTFjMWE1IiwiZmlyc3ROYW1lIjoiIiwibGFzdE5hbWUiOiIiLCJlbWFpbCI6IiIsImlzQW5vbnltb3VzIjp0cnVlLCJiZWhhdmlvcnMiOlsxMDE0XX0sInVzZXJQcm9maWxlIjp7InVzZXJJZCI6ImRlNDQyZmZmMGI1YjRmZDViOWZlMGQ1ZmI1YTFjMWE1IiwiZmlyc3ROYW1lIjoiIiwibGFzdE5hbWUiOiIiLCJlbWFpbEFkZHJlc3MiOiIiLCJ1c2VyTmFtZSI6IiJ9LCJpc0VkaXRNb2RlIjpmYWxzZSwiaXNBZG1pbk1vZGUiOmZhbHNlLCJub3ciOiIyMDE5LTA4LTA3VDA5OjA5OjI5LjQzNjE4NzNaIiwiY3Jhd2xlckluZm8iOnsiaXNDcmF3bGVyIjpmYWxzZX0sImN1cnJlbmN5UmF0ZUluZm8iOnt9fQ%3d%3d',
        'if-none-match': '0ae17e4274044262b12ae7182a92d89a',
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"}
    request = requests.get(url, headers=headers)
    store_list = json.loads(request.text)['items']
    for store in store_list:
        output = []
        storeHours = ""
        hour_flag = True
        for x in list(store.get('regularHours').keys()):
            if store.get('regularHours')[x].get('label'):
                hour_flag = False
            storeHours += x + u' ' + store.get('regularHours')[x].get('label') + u','
        storeHours = storeHours[:-1]
        if hour_flag:
            storeHours = 'Assortment and hours vary by store. Please contact the store for additional information.'
        output.append(base_url)
        output.append(store.get('name'))
        output.append(store.get('address').get('address1'))
        output.append(store.get('address').get('cityOrTown'))
        output.append(store.get('address').get('stateOrProvince'))
        output.append(store.get('address').get('postalOrZipCode'))
        output.append('US')
        output.append(store.get('code'))
        output.append(store.get('phone'))
        output.append(store.get('locationTypes')[0].get('name'))
        output.append(store.get('geo').get('lat'))
        output.append(store.get('geo').get('lng'))
        output.append(storeHours)
        pdb.set_trace()
        output_list.append(validate(output))
    return output_list
    
def scrape():
    data = fetch_data()
    write_output(data)

scrape()
