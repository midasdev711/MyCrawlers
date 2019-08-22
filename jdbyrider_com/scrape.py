import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'https://www.jdbyrider.com'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').encode("utf8").strip()

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
    url = "https://www.jdbyrider.com/wp-admin/admin-ajax.php?action=get_locations_details&locIds=AL106%2CFL161%2CFL163%2CAR102%2CAR101%2CAR103%2CAR104%2CAZ103%2CAZ109%2CCO107%2CCT103%2CFL139%2CFL154%2CFL162%2CIA104%2CIA109%2CIA110%2CIA111%2CMO106%2CMO109%2CMO113%2CID101%2CIL105%2CIL116%2CIL115%2CIL121%2CIL125%2CIL131%2CIL117%2CIL119%2CIL122%2CIL124%2CILC40%2CINC39%2CIN115%2CINC02%2CINC03%2CINC05%2CINC07%2CINC10%2CKYC20%2COH105%2COH112%2COH127%2COH134%2COH143%2COH144%2COH145%2COH150%2COHC09%2COHC11%2COHC12%2COHC13%2COHC18%2COHC19%2CPA103%2CPA104%2CPA112%2CPA113%2CPA114%2CTN107%2CIN116%2CIN116A%2CIN116B%2CIN116C%2CIN116D%2CIN116H%2CMO110%2CKY104%2CMI115%2CIN125%2CMA102%2CMA108%2CMD102%2CIN124%2CMI105%2CMI108%2CMI109%2CMI113%2CMN104%2CMO112%2CMS104%2CMS105%2CNC112%2CNH101%2CNY107%2COH122%2CKY107%2CWV104%2CWV105%2CWV106%2CWV107%2CWV109%2COH130%2COH140%2COH142%2COH148%2COH152%2COH132%2CPA110%2CFL164%2CPA108%2CPA111%2CPA115%2CPA116%2CPA117%2CMA103%2CMA104%2CMA105%2CRI101%2CSC105%2CSC114%2CSC115%2CTN109%2CTX109%2CTX115%2CTX116%2CTX112%2CTX114%2CTX122%2CTX118%2CTX126%2CTX127%2CUT104%2CVA102%2CWI102%2CWI104%2CWI107%2CWI110%2CWI112%2CWI111%2CWI115%2CWI114%2CKY106%2CWV108%2CCO108%2CIL132%2CTX128%2COH154%2CID102%2CPA101%2CAL112%2CWI116%2CMD106%2CTNC41%2CLA108%2CWI117%2CBDNC01%2CBDNC02"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "_gcl_au=1.1.827859710.1565813472; _ga=GA1.2.1948042990.1565813472; _gid=GA1.2.543638037.1565813472; _mibhv=anon-1565813471977-7908663290_7750; _micpn=esp:-1::1565813471977; _vwo_uuid_v2=D41BC469009808A6668AB77B91FAE906C|543d7e58a1f74df1b8a8b5216aafa97a; PHPSESSID=48d2f59d8afa1543f339f81fe2979b6b; lead_id=F4B77F7D-A1D7-04CD-C72B-BF6D1C76CE04; _fbp=fb.1.1565813473462.2061726676; _vis_opt_s=1%7C; _vis_opt_test_cookie=1; _vwo_uuid=D41BC469009808A6668AB77B91FAE906C; _vwo_ds=3%3Aa_0%2Ct_0%3A-1%241565813471%3A21.35738044%3A%3A27_0%2C26_0%2C25_0%2C24_0%2C23_0%2C22_0%2C21_0%2C20_0%2C19_0%2C18_0%2C16_0%2C15_0%3A70_0%2C28_0%2C23_0%2C1_0%3A0; _vwo_sn=0%3A6",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    request = requests.get(url, headers=headers)
    store_list = json.loads(request.text)
    keys = list(store_list.keys())
    store_hours = ""

    for key, store in store_list.items():
        if store:
            hours = store['_ServiceHours']
            for hour in hours:
                if hour['isClosed']:
                    store_hours += hour["dayOfWeek"] + ": Closed "
                else:
                    store_hours += hour["dayOfWeek"] + ":" + hour["openTime"] + ' - ' + hour["closeTime"] + " "
            output = []
            output.append(base_url) # url
            output.append(get_value(store['_BusName'])) #location name
            output.append(get_value(store['_BusAddr1'])) #address
            output.append(get_value(store['_BusCity'])) #city
            output.append(get_value(store['_BusStateCd'])) #state
            output.append(get_value(store['_BusZipCd'])) #zipcode
            output.append('US') #country code
            output.append(key) #store_number
            output.append(get_value(store['_ServicePhoneNumber'])) #phone
            output.append(validate(store["_SrvType"])) #location type
            output.append(store['latitude']) #latitude
            output.append(store['longitude']) #longitude
            output.append(validate(store_hours)) #opening hours
            if store['location_is_closed']:
                continue        
            output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
