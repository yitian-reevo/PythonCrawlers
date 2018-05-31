import requests
import re
import json
import time
from random import choice
import configure

url = "http://maoyan.com/board/4"
header = {'user-agent': choice(configure.FakeUserAgents)}
movielist = []

def OnePageSpider(url = url):
	try:	
		response = requests.get(url, headers=header)
		content = None

		if response.status_code == requests.codes.ok:
			content = response.text

	except RequestException as e:
		print (e)
		return

	# '.*?class="borad-img" src="(.*?)"'	
	pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>'
        '.*?<img data-src="(.*?)"'
        '.*?class="name"><a.*?>(.*?)</a>'
        '.*?class="star">(.*?)</p>'
        '.*?class="releasetime">(.*?)</p>'
        '.*?class="score"><i class="integer">(.*?)</i><i class="fraction">(.*?)</i>'
        '.*?</dd>', re.S)

	items = pattern.findall(content)
	for item in items:
		movie = {}
		movie['id'] = item[0]
		movie['image'] = item[1]
		movie['name'] = item[2]
		movie['star'] = item[3].strip()[3:] #去除空格和\n符
		movie['release_time'] = item[4][5:]
		movie['score'] = item[5] + item[6]
		movielist.append(movie)
		
if __name__ == '__main__':
	OnePageSpider()

	# 这里取巧了，抓取下一页也是可以的。
	for i in range(10, 100, 10):
		OnePageSpider(url + "?offset={0:d}".format(i))
		time.sleep(0.5)

	# 这里有个编码问题，像我这么写可以解决
	with open('top100.json', 'w', encoding = 'utf-8') as file:
		for movie in movielist:
			file.write(json.dumps(movie, ensure_ascii = False) + '\n')			
