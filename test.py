import json

import requests
from bs4 import BeautifulSoup
import urllib.parse as urlparse


def test():
    url = 'https://www.grohe.com.tr/solr/master_tr_TR_Product/select?defType=edismax&facet.limit=1000&fl=pl_displayName,communicationDesign,modelName,code,category&fq=(b2cAssortment:true OR b2bAssortment:true) AND category:(Shower OR 005-SH-0560-G480_master_en_Product OR 005-SH-0560-G505_master_en_Product OR 005-SH-0560-G506_master_en_Product)&q=*:*&qf=code^40.0 communicationDesign^20.0 fulltext webSiteEndUserShort claim&rows=20&sort=pl_displayName asc&start=0&wt=json'
    parsed = urlparse.urlparse(url)
    x = urlparse.parse_qs(parsed.query)['fq'][0].translate(str.maketrans({
        '(': '',
        ')': ''
    })).split(sep=':')

    print(x)


if __name__ == '__main__':
    test()
