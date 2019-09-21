import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress

base_url = 'https://www.zgallerie.com'

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

def parse_address(address):
    address = usaddress.parse(address)
    street = ''
    city = ''
    state = ''
    zipcode = ''
    country = ''
    for addr in address:
        if addr[1] == 'PlaceName':
            city += addr[0].replace(',', '') + ' '
        elif addr[1] == 'ZipCode':
            zipcode = addr[0].replace(',', '')
        elif addr[1] == 'StateName':
            state = addr[0].replace(',', '')
        elif addr[1] == 'CountryName':
            country = addr[0].replace(',', '')
        else:
            street += addr[0].replace(',', '') + ' '

    return { 
            'street': get_value(street), 
            'city' : get_value(city), 
            'state' : get_value(state), 
            'zipcode' : get_value(zipcode),
            'country': get_value(country)
            }

def fetch_data():
    output_list = []
    url = "https://www.zgallerie.com/storelocations.aspx/GetStoreAddresses"
    state_list = ["AK","AL","AR","AZ","CA","CO","CT","DE","FL","GA","HI","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VA","VT","WA","WI","WV","WY"]
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Cookie": '.ASPXANONYMOUS=uGiqlEOe1QEkAAAAYWEzNTdkZjEtYWM5MS00ZjRiLWE2NzMtZjZiYjg3ZmU1OTEzNssuYlQM3R5nTZS7lFRC7yQKSDk1; ASP.NET_SessionId=katjcu55phhjpprapkge3c45; _svsid=0694ad251a210e8db7330dc02396038e; crl8.fpcuid=3ca93320-7f19-4ef4-b922-38f0ff2c2422; _gcl_au=1.1.1680944069.1568104084; _FPAC_S=_pk_ses.37770.b600=*|_pk_ses.37804.b600=*; ltkSubscriber-BCFooter=eyJsdGtUcmlnZ2VyIjoibG9hZCJ9; trustedsite_visit=1; _ga=GA1.2.2019380242.1568104086; _gid=GA1.2.1127032570.1568104086; tracker_device=59635cc1-6270-4241-a348-cad24a99e1a0; ltkpopup-suppression-4141df93-0220-4121-88c9-b0f200a673a9=1; MGX_P=96782d76-1846-4d97-a1b1-72de6bfd200e; MGX_U=61e850d8-4e3e-44d5-9a8d-05e1e43254da; MGX_PX=c877fab8-392b-4d75-b97b-618ea3b97b5a; MGX_CID=127945ab-7b2a-4d77-ab5b-2fd0985baac4; cto_lwid=0ee42a12-c8fb-48de-b1da-ddcdbff36223; GSIDEmCC5iEfX18F=1002d037-a4f3-4d9c-9cff-350c2cc4d39f; STSID830653=6064eb95-d721-4d08-9a34-50155d857e3f; _ga_tng=GA1.3.1621794575.1568104091; _ga_tng_gid=GA1.3.847077417.1568104091; tangiblee:widget:user=c162c946-801d-4b2f-b088-08fb3eea8933; _vuid=c5161b42-3ada-4a2d-858c-04045246c800; _hjid=98cf9185-0507-4592-b14a-f527030678b6; _hjIncludedInSample=1; _fbp=fb.1.1568104094225.1957851648; MGX_EID=bnNfc2VnXzAwMA==; __qca=P0-294290435-1568104091391; com.silverpop.iMAWebCookie=de2d4d28-16c3-778b-7d51-8c325e456622; _aeaid=370f4710-f3d4-49e6-bc28-7d3ad98a2616; aedinkplayed=true; aeatstartmessage=true; ltkpopup-session-depth=2-3; _FPCI={"fingerPrint":"1568104080390NKUAjYZtbnZAavPgWNQ","lastActionTime":1568104243,"visitCount":1,"IsMobile":false,"DeviceType":"Desktop","IsCrawler":false,"HardwareName":["Desktop","Emulator"],"HardwareVendor":"Unknown","PlatformName":"Windows","PlatformVendor":"Microsoft","PlatformVersion":"10.0","BrowserName":"Chrome","BrowserVendor":"Google","BrowserVersion":"67","IsSmallScreen":false,"IsSmartPhone":false,"IsSmartWatch":false,"IsTablet":false,"IsTv":false,"IsMediaHub":false,"IsConsole":false,"IsEReader":false,"version":"0.3","visitorId":"1097597515"}; _FPAC=_pk_id.37770.b600=3655a574b64716c5.1568104084.1.1568104244.1568104084.|_pk_id.37804.b600=27d153020c80c18f.1568104084.1.1568104244.1568104084.; MGX_VS=3; AWSELB=8F773B130A1A30C5A2C22590D257B2AB23CA8A1AE66373982C9917B6EEFD54CC3284B6BB52C197BAB86DA97BCE9960A7BF14B01673EBF623BE29F0BF6B44864C0F7C706BEB; _gat_UA-3580289-6=1; _gali=browser',
        "Host": "www.zgallerie.com",
        "Origin": "https://www.zgallerie.com",
        "Referer": "https://www.zgallerie.com/storelocations.aspx",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    for state in state_list:
        payload = {
            "City": "",
            "State": state,
            "Type": "state"
        }
        request = requests.post(url, json=payload)
        response = json.loads(request.text)['d']
        store_list = etree.HTML(response).xpath('.//div[@class="found_location_details"]')
        for store in store_list:
            info = eliminate_space(store.xpath('.//div[@class="left"]//text()'))
            hours = get_value(store.xpath('.//div[@class="middle"]//text()'))
            geoinfo = validate(store.xpath('.//input/@value'))
            latitude = geoinfo.split('|')[0]
            longitude = geoinfo.split('|')[1]
                
            output = []
            output.append(base_url) # url
            output.append(info[0]) #location name
            output.append(info[1]) #address
            output.append(info[2].split(', ')[0]) #city
            output.append(info[2].split(', ')[1].split(' ')[0]) #state
            output.append(info[2].split(', ')[1].split(' ')[1]) #zipcode
            output.append(validate('US')) #country code
            output.append('<MISSING>') #store_number
            output.append(info[3]) #phone
            output.append("Decor Store | Affordable & Modern Furniture | Z Gallerie") #location type
            output.append(latitude) #latitude
            output.append(longitude) #longitude
            output.append(hours.replace('Hours:', '')) #opening hours
            output_list.append(output)

    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
