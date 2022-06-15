import json
import time
import requests
import ast
import urllib.parse
from bs4 import BeautifulSoup
from tqdm import tqdm


def main_url(limit=1000, rows=1, start=0):
    url = f'https://www.grohe.com.tr/solr/master_tr_TR_Product/select?defType=edismax&facet.limit={limit}&facet.mincount=1&facet.query=bim:*&facet.query=-bim:*&fl=modelName,category,communicationDesign,pl_displayName,code&fq=(b2cAssortment:true OR b2bAssortment:true) AND category:Washbasin&indent=true&q=*:*&qf=code^40.0 communicationDesign^20.0 fulltext webSiteEndUserShort claim&rows={rows}&sort=pl_displayName asc&start={start}&wt=json'
    return url


def num_found():
    x = requests.get(main_url())
    x = x.json()
    x = x['response']['numFound']
    return x


def productData():
    base_url = 'https://www.grohe.com.tr/tr_tr/'
    # s = [200, 240]
    bar = tqdm(range(num_found()), colour='#18f763', unit=' loading...')
    dizi = []
    for s in bar:
        products = {
            'index': '',
            'displayName': '',
            'modelName': '',
            'categories': '',
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
        product_categories = x['category']
        product_name = x['modelName']
        name_url = urllib.parse.quote(x['modelName'], safe="'")
        product_code = x['code']
        url = base_url + serial_name + '-' + name_url + '-' + product_code + '.html'
        products['index'] = s
        products['displayName'] = serial_name
        products['modelName'] = product_name
        products['categories'] = product_categories
        products['code'] = product_code
        products['url'] = urllib.parse.quote(url, safe='://')
        dizi.append(products)
        bar.set_description(product_code)
    # fname -> Specify new filename
    jsonWrite('', dizi)
    print(dizi)


def jsonWrite(fname, data):
    js = json.dumps(data, ensure_ascii=False, indent=4)
    with open(f"{fname}.json", "w", encoding='utf-8') as outfile:
        outfile.write(js)


if __name__ == '__main__':
    productData()
