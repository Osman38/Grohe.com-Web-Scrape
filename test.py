from pysitemap import crawler
import logging
import sys
from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as ET


def sitemap():
    # if '--iocp' in sys.argv:
    #     sys.argv.remove('--iocp')
    #     logging.info('using iocp')
    #     el = windows_events.ProactorEventLoop()
    #     events.set_event_loop(el)
    root_url = 'https://www.haikson.com'
    x = crawler(root_url, out_file='test.xml', exclude_urls=[".css","contakts",";{%","&quot"])
    return x


def xmlRead():
    content = []
    liste = []
    with open("test.xml", "r") as file:
        content = file.readlines()
        content = "".join(content)
        bs_content = BeautifulSoup(content, "xml")
        x = bs_content.find_all('loc')

        for y in x:
        #     dizi = ['.css', 'page', 'web-content']
        #     for d in dizi:
        #         if re.search(d, y.text) != None:
        #             pass
        #         else:
        #             # print(y.text)
        #             liste.append(y.text)
        # print(liste)
            print(y.text)


def reg():
    txt = "Türkiye'de yağmur"
    x = re.search("kanada", txt)
    if x == None:
        pass
    return x


def GenerateXML():
    import xml.etree.ElementTree as ET
    tree = ET.parse('test.xml')
    root = tree.getroot()
    print(root.tag)


if __name__ == '__main__':
    xmlRead()
