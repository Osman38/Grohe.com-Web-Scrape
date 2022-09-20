import json
import time

import psycopg2

from psycopg2.extras import RealDictCursor


def connection(host, database, user, password):
    while True:

        try:
            conn = psycopg2.connect(host=host, database=database, user=user, password=password)
            conn.autocommit = True
            cursor = conn.cursor()
            # print('DB Connection : Database connection was successfull')
            return cursor
            # break
        except Exception as error:
            print('DB Connection : Connecting to database failed')
            print('Error : ', error)
            time.sleep(2)


def insertData():
    file = open('newJson.json', encoding='utf8')
    x = json.load(file)
    # s= 75
    for s in range(len(x)):
        product_url = x[s]['url']
        product_name = x[s]['name']
        product_code = x[s]['code']
        ean = x[s]['ean']
        category = x[s]['categories']
        color = x[s]['color']
        price = x[s]['price']
        description = str(x[s]['description'])
        features = x[s]['features']
        image = x[s]['images']
        z = connection(host='localhost',database='products',user='postgres',password='123456')
        insert_data = "insert into products (product_url,name,product_code,ean,category,color,price,description,features,image) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        if price == 'Null':
            price = 0
        else:
            price = price.replace('.', '').replace(',', '.')
        data = (product_url, product_name, product_code, ean, category, color, price,
                description, features, image)
        z.execute(insert_data, data)

        print(s)


def testQuery():
    x = connection(host='localhost',database='products',user='postgres',password='123456')
    x.execute("select * from products WHERE product_code='22037DA0'")
    y = x.fetchall()
    print(y)


if __name__ == '__main__':
    testQuery()
