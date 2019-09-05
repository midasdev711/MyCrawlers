import csv
import re
import pdb
import requests
from lxml import etree
import json
import usaddress


base_url = 'https://www.raleys.com'

def validate(item):    
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').encode("utf8").strip().replace('\n', '').replace('\t\t', '')

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
    url = "https://www.raleys.com/store-locator/?search=all"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "nlbi_241206=T4cKC4dRUVe5hAEI2nnEYQAAAABk4sTkYxa7gioJ/GZCz7md; visid_incap_241206=L/6X1VOwQ42IcIJmYqV3UGuhUV0AAAAAQUIPAAAAAAC0TOosjlbnrcIMAGi+EXMv; incap_ses_676_241206=Z0GDJKH9dALH600co6NhCWuhUV0AAAAAZstwNDuZQ8lpJ4uKWjtATg==; _gcl_au=1.1.1510972846.1565630832; _ga=GA1.2.1112933338.1565630832; _gid=GA1.2.618574610.1565630832; _gat_UA-72342337-4=1; _gat_UA-1619466-1=1; _fbp=fb.1.1565630833638.2028457922; visid_incap_802681=7C9bK3fIRyS5CtD9iYi0NHKhUV0AAAAAQUIPAAAAAAAvrSr3j50PdKdcvmPpbW5p; incap_ses_672_802681=2jSqVodn1GF8zR/lnG1TCXKhUV0AAAAAP3BFAGg44LAaz6zhDuNw+Q==; gig_hasGmid=ver2; session-ray=.eJxNzE1rgzAAxvHvknMpJn1h8ba2w0UaXbfZiBdJasREE4vRio5997nDYIfn8uPh_wXyspOuAn7JGydXIL_LznArbQ_8vhsWcdI51dq8b2tpgQ_kFFYiuKlYhSSZCYxUiNe_mAXwLux1ztKw5OyiYrODIhgd-W_6BdG5nujpMp2PS8jgQTL4KFKqYvs-FSz5-y-LZs7wkKKmJrqF0em2jXSyiV-9tRFG68OoD5L2UD0fszeK9qzyGh4I_Pl4Iuer3tkqGT9asAKDk12uCuDD_QYjb4u-fwB4_VTu.EDMy9Q.B9Tr0oyloMMvjUw_LLVgWR0zWYQ; liveagent_oref=; liveagent_ptid=ca365852-68f0-466d-853b-5eeea6807667; liveagent_sid=c246d5fb-ff54-44d0-92b0-4755c7a55575; liveagent_vc=3",
        "Host": "www.raleys.com",
        "Referer": "https://www.raleys.com/store-locator/",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    request = requests.get(url, headers=headers)
    response = etree.HTML(request.text)
    store_list = response.xpath('//ol[@class="stores-list"]/li')
    for store in store_list:
        address = store.xpath('.//address/text()')[0]
        address = usaddress.parse(address)
        street = ''
        city = ''
        state = ''
        zipcode = ''
        for addr in address:
            if addr[1] == 'PlaceName':
                city += addr[0].replace(',', '') + ' '
            elif addr[1] == 'ZipCode':
                zipcode = addr[0]
            elif addr[1] == 'StateName':
                state = addr[0]
            else:
                street += addr[0].replace(',', '') + ' '
        phone = get_value(store.xpath('.//ul[@class="contact-list"]//text()'))
        phone = phone.replace('Store:  () -', '').replace('Pharmacy:  () -', '')
        phone = get_value(phone)
        store_hours = get_value(store.xpath('.//div[@class="box"]')[0].xpath('.//text()'))

        output = []
        output.append(base_url) # url
        output.append(validate(store.xpath('.//h2/text()'))) #location name
        output.append(get_value(street)) #address
        output.append(get_value(city)) #city
        output.append(get_value(state)[:2]) #state
        output.append(get_value(zipcode)) #zipcode
        output.append('US') #country code
        output.append('<MISSING>') #store_number
        output.append(phone) #phone
        output.append("Stores Archive - Raley's Family of Fine Store") #location type
        output.append(get_value(store.xpath('./@data-lat'))) #latitude
        output.append(get_value(store.xpath('./@data-lng'))) #longitude
        output.append(store_hours) #opening hours
        output_list.append(output)
    return output_list

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
