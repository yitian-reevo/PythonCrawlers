import re
import time
import redis
import execjs
from bs4 import BeautifulSoup
from urllib import parse
import ohRequests as requests
#import requests

URLS = [
    'https://www.dm5.com/search?title=Marvel+Comics+&language=1&f=2',
    'https://www.dm5.com/search?title=DC&language=1&page=1'
]

BOOK_URLS = []

DOMAIN = "https://www.dm5.com"


def index_page_parser(url):
    req = requests.ohRequests()
    headers = {
        'Referer':
            'https://www.dm5.com/manhua-bianfuxia-fuzhizuiqian'
        }

    content = req.get(url, headers=headers, verify=False)

    soup = BeautifulSoup(content, 'lxml')

    mh_list = soup.find_all('ul', class_='mh-list')[0]
    mh_items = mh_list.find_all('li')

    for mh_item in mh_items:
        BOOK_URLS.append(DOMAIN + mh_item.find('a').get('href'))

    pager = soup.find_all('div', class_='page-pagination')[0]
    pager = pager.find_all('li', text=re.compile('>'))

    if not pager:
        return None

    return DOMAIN + pager[0].a.get('href')

def book_page_parser(url):
    req = requests.ohRequests()
    headers = {
        'Referer':
            'https://www.dm5.com/manhua-bianfuxia-fuzhizuiqian'
        }

    content = req.get(url, headers=headers, verify=False)

    soup = BeautifulSoup(content, 'lxml')

    view_win_list = soup.find_all('ul', class_='view-win-list')[0]

    chapter_list = view_win_list.find_all('li')

    for chapter in chapter_list:
        a = chapter.a
        #span = chapter.a.span.text.strip()
        #n = re.findall('\d+', span)

        print (a.text.replace(' ', ''), DOMAIN + a.get('href'))
    

def chapter_page_parser(url, n):
    req = requests.ohRequests()
    headers = {
        'Referer':
            'https://www.dm5.com/manhua-bianfuxia-fuzhizuiqian'
        }

    content = req.get(url, headers=headers, verify=False)

    pattern = re.compile(
        '.*?DM5_MID=(.*?);'
        '.*?DM5_CID=(.*?);'
        '.*?DM5_IMAGE_COUNT=(.*?);'
        '.*?DM5_VIEWSIGN=(.*?);'
        '.*?DM5_VIEWSIGN_DT=(.*?);.*?'
        , re.S)

    mid, cid, image_count, sign, date = pattern.findall(content)[0]

    for i in range(1, int(image_count)):
        url = "https://www.dm5.com/m192438/chapterfun.ashx?cid={0:s}&page={1:d}&key=&language=1&gtk=6&_cid={2:s}&_mid={3:s}&_dt={4:s}&_sign={5:s}".format(
            cid, i, cid, mid, date.replace('"',''), sign.replace('"','')
            )
        r = req.get(url, headers=headers, verify=False)
        r = r.replace('eval(','')[:-2]
        
        js = "function run(){{return {0:s}}}".format(r)
        print (js)
        ctx = execjs.compile(js).call('run')
        print (ctx)
        ctx = execjs.compile(ctx).call('dm5imagefun')
        print (ctx)
        print (js)
        print (ctx[0])
        break

    

def image_downloader(image_url):
    pass

def main():
    """
    ret = index_page_parser(URLS[1])
    while True:        
        if not ret:
            break
        print (ret)
        ret = index_page_parser(ret)
        time.sleep(0.5)

    print (len(BOOK_URLS))
    

    url = "https://www.dm5.com/manhua-dcyzvsyzdjrxm/"
    book_page_parser(url)
    """

    url = "https://www.dm5.com/m192438/"
    chapter_page_parser(url, 22)

if __name__ == "__main__":
    main()