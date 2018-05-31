import re
import time
import aiohttp
import asyncio
from bs4 import BeautifulSoup

import ohSqlite3 as sqlite
import ohRequests as requests

DB_NAME = "aqicn.db"
URLS_LIST = []

def db_init():
    req = requests.ohRequests()
    content = req.get("http://aqicn.org/city/all/cn/")
    
    pattern = re.compile("中国</div><br>(.*?)五家渠农水大厦</a>", re.S)
    data = pattern.findall(content)[0] + "五家渠农水大厦</a>"

    soup = BeautifulSoup(data, 'lxml')

    links = soup.find_all('a')

    with sqlite.ohSqlite3(DB_NAME) as db:
        #db.execute("CREATE TABLE aqicn (location text, url text)")
        #for link in links:
        #    db.execute("INSERT INTO aqicn VALUES (?,?)", (link.text, link.get('href'),))
        #db.execute("DELETE FROM aqicn WHERE location = ' '")
        pass 

def parser_single(location, url):
    req = requests.ohRequests()
    content = req.get(url)
 
    pattern = re.compile('<table class=\'api\'(.*?)</table>', re.S)
    data = pattern.findall(content)

    if data:
        data = "<table class='api' {} </table>".format(data[0])
    soup = BeautifulSoup(data, 'lxml')

    aqi = soup.find(id='aqiwgtvalue').text

    if aqi == '-':
        return None

    t = soup.find(id='aqiwgtutime').get('val')

    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t)))

    return [location, aqi, t]

async def parser():
    req = requests.ohRequests()
    while URLS_LIST:
        url = URLS_LIST.pop(0)
        header = {'user-agent': req.faker_user_agent()}

        async with aiohttp.ClientSession() as session:
            async with session.get(url[1], headers=header) as response:
                content = await response.text()
        
        pattern = re.compile('<table class=\'api\'(.*?)</table>', re.S)
        data = pattern.findall(content)

        if not data:
            print ("Something is wrong. Might be station removed:[{}]({})".format(url[0], url[1]))
            continue

        data = "<table class='api' {} </table>".format(data[0])
        soup = BeautifulSoup(data, 'lxml')

        aqi = soup.find(id='aqiwgtvalue').text

        if aqi == '-':
            print ("No Data:[{}]({})".format(url[0], url[1]))
            continue

        t = soup.find(id='aqiwgtutime').get('val')

        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t)))

        print ([url[0], aqi, t])


def main():
    global URLS_LIST
    req = requests.ohRequests()

    with sqlite.ohSqlite3(DB_NAME) as db:
        URLS_LIST = db.execute("select * from aqicn")


    coroutine_cnts = 50
    t = time.time()
    
    coros = []
    loop = asyncio.get_event_loop()
    for i in range(coroutine_cnts):
        coros.append(parser())

    loop.run_until_complete(asyncio.gather(*coros))

    print ("Total {}s".format(time.time()-t))

def tofile():
    with sqlite.ohSqlite3(DB_NAME) as db:
        items = db.execute("select * from aqicn")

    print (items)
    with open("urls.txt", 'w', encoding='utf-8') as file:
        for item in items:
            file.write("{},{}\n".format(item[0], item[1 ]))

if __name__ == "__main__":
    #db_init()
    #main()
    tofile()