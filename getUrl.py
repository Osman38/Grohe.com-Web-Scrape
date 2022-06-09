import json
import time

import requests
import ast
import urllib.parse
from bs4 import BeautifulSoup
from tqdm import tqdm


def main_url(limit=1000, rows=1, start=0):
    url = f'https://www.grohe.com.tr/solr/master_tr_TR_Product/select?defType=edismax&facet.limit={limit}&facet.mincount=1&facet.query=bim:*&facet.query=-bim:*&fl=modelName,communicationDesign,pl_displayName,code&fq=(b2cAssortment:true OR b2bAssortment:true) AND category:Washbasin&indent=true&q=*:*&qf=code^40.0 communicationDesign^20.0 fulltext webSiteEndUserShort claim&rows={rows}&sort=pl_displayName asc&start={start}&wt=json'
    return url


def num_found():
    x = requests.get(main_url())
    x = x.json()
    x = x['response']['numFound']
    return x


def getJsonData():
    x = requests.get(main_url(limit=num_found(), rows=num_found()))
    x = x.text
    with open("test.json", "w", encoding='utf-8') as outfile:
        outfile.write(x)
    return 'Success Full'


def writeJsonData():
    base_url = 'https://www.grohe.com.tr/tr_tr/'
    # s = [200, 240]
    bar = num_found() - 1
    dizi = []
    for s in tqdm(range(bar), colour='#18f763'):

        products = {
            'index': '',
            'displayName': '',
            'modelName': '',
            'code': '',
            'url': ''
        }
        x = requests.get(main_url(limit=num_found(), start=s))
        x = x.json()
        x = x['response']['docs'][0]
        try:
            serial_name = ast.literal_eval(x['communicationDesign'][0])['displayName'].replace(' ', '-')
        except KeyError:
            try:
                serial_name = x['pl_displayName'].replace(' ', '-')
            except KeyError:
                serial_name = ''

        product_name = x['modelName']
        name_url = urllib.parse.quote(x['modelName'], safe="'")

        # print(product_name)
        product_code = x['code']
        url = base_url + serial_name + '-' + name_url + '-' + product_code + '.html'
        # print(url)
        products['index'] = s
        products['displayName'] = serial_name
        products['modelName'] = product_name
        products['code'] = product_code
        products['url'] = urllib.parse.quote(url, safe='://')
        dizi.append(products)
        # print(s, ':', products)

    js = json.dumps(dizi, ensure_ascii=False, indent=4)

    with open("test-2.json", "w", encoding='utf-8') as outfile:
        outfile.write(js)
    print(dizi)


def jsonProductLink(s=0):
    f = open('test-2.json', encoding='utf-8')
    data = json.load(f)
    url = data['products'][s]['url']
    return url


def test():
    l = num_found()
    for i, e in tqdm(range(l), total=num_found()):
        time.sleep(1)
        print(i)


if __name__ == '__main__':
    writeJsonData()
