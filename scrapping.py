import json
import requests
from bs4 import BeautifulSoup
import urllib.parse
from tqdm import tqdm, trange, tqdm_notebook

import getUrl


def jsonData(s=0):
    f = open('newUrl.json', encoding='utf-8')
    data = json.load(f)
    url = data[s]['url']
    categories = data[s]['categories']
    return [url, categories]


def pageSource(url):
    req = requests.get(url)
    page = BeautifulSoup(req.content, 'html.parser')
    return page


def productData():
    dizi = []
    i = getUrl.num_found()
    try:
        for s in tqdm(range(i), desc='loading...', colour='#00ff0a'):
            url = jsonData(s)[0]
            page = pageSource(url)
            # print(url)
            img_list = []
            product_dict = {
                'index': '',
                'url': '',
                'name': '',
                'code': '',
                'ean': '',
                'categories': '',
                'color': '',
                'price': '',
                'description': '',
                'features': '',
                'images': ''
            }
            try:
                product_name = page.find('meta', attrs={'name': 'title'}).get('content').title()
            except AttributeError:
                product_name = page.find('h1', attrs={'itemprop': 'name'}).text
            product_code = page.find('div', attrs={'class': 'product-box__tableCell--value'}).getText()
            ean_code = page.select_one(
                'div > div.product-box__table > div:nth-child(2) > div.product-box__tableCell.product-box__tableCell--value').text

            try:
                product_color = page.select_one(
                    'div > div.product-box__table > div:nth-child(3) > div.product-box__tableCell.product-box__tableCell--value').text.strip().title()
            except AttributeError:
                product_color = 'No Color'
            try:
                product_price = page.find('div', attrs={'class': 'product-box__price'}).find('strong').text.strip()
            except AttributeError:
                product_price = 'Null'
            try:
                product_detail = page.select_one(
                    '#vuejs-main-container > article > section.stripe.stripe--lightgray.pdp__section-tabs > div > div > div')
                desc = {
                    'title': product_detail.select_one('h3').text.title(),
                    'description': product_detail.select_one('div>p').text.replace('\n', ' ')
                }
            except AttributeError:
                desc = 'Null'
            try:
                product_features = page.find('ul', attrs={'class': 'list'}).text.strip()
            except AttributeError:
                product_features = 'Null'
            try:
                images = page.find('swiper-connector').findAll('a')
                for a in images:
                    z = a.get('href')
                    img_list.append(z)
            except AttributeError:
                images = page.find('div', attrs={'class': 'product-image-container'}).find('a').get('href')
                img_list.append(images)

            product_dict['index'] = s
            product_dict['url'] = url
            product_dict['name'] = product_name
            product_dict['code'] = product_code
            product_dict['ean'] = ean_code
            product_dict['categories'] = jsonData(s)[1]
            product_dict['color'] = product_color
            product_dict['price'] = product_price
            product_dict['description'] = desc
            product_dict['features'] = product_features.replace('\n', ', ')
            product_dict['images'] = img_list

            dizi.append(product_dict)

            # print(
            #     f'id : {s + 1}\nÜrün Adı : {product_name}\nÜrün Kodu : {product_code}\nEAN : {ean_code}\nRenk : {product_color}\nÜrün Fiyatı : {product_price}\nÜrün Açıklaması : {desc}\nÜrün Özellikleri : {product_features}\nÜrün Resimleri : {img_list}')
            # print(f"{product_dict['index']} - {url}")
            # s += 1
    except IndexError:
        pass

    getUrl.jsonWrite(fname='newJson', data=dizi)


if __name__ == '__main__':
    productData()
