import requests
import re
import json
import time
from random import choice
from bs4 import BeautifulSoup
import Configure


header = {'user-agent': choice(Configure.FakeUserAgents)}

cookies = {}
cookiestr = '''
			BAIDUID=42F6DD1CC8665CEF88C2A26C1F0F504C:FG=1; 
			BIDUPSID=42F6DD1CC8665CEF88C2A26C1F0F504C; 
			PSTM=1524011246; TIEBA_USERTYPE=18f315073eddae18a6dfa5f6; 
			bdshare_firstime=1524016473188; 
			Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1524016474,1524173313,1524593010; 
			FP_UID=2143bdc5c13bdcf8b476c96453c42b93; 
			pgv_pvi=7109722112; 
			BDUSS=1lzbm12RGVHOTF5emNMOVRTVnY1VHlydlNUR0QtS29hZ0h0S0RhY1dhaFNhQTliQVFBQUFBJCQAAAAAAAAAAAEA
				AABo44AfWmlvbjEyMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
				AAAAFLb51pS2-daY; 
			cflag=15%3A3; 
			TIEBAUID=08df9b3ba5f5e5335cf67ff4; 
			STOKEN=a97aaf8a8e0724638e351933aaeed3bd4edf2dad29bc8f83a88e94b4738958ee; 
			wise_device=0; 
			Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1525205956,1525334517,1525371306,1525372116; 
			528540520_FRSVideoUploadTip=1; 
			Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1525372413
			'''

for cookie in cookiestr.split(';'):
    name,value=cookie.strip().split('=',1)  
    cookies[name]=value

# 获取精品帖子的页数
def getGoodCount():
	url = "http://tieba.baidu.com/f"
	payload = {
	    'kw':'复仇者联盟',
	    'ie':'utf-8',
	    'tab':'good'
	}
	try:
		response = requests.get(url, headers=header, params=payload, cookies=cookies)
		content = None

		if response.status_code == requests.codes.ok:
			content = response.text
			
	except Exception as e:
			print (e)

	pattern_next = re.compile('共有精品数.*?(\d+).*?个', re.S)
	data = pattern_next.findall(content)

	return (int(data[0]))

# 获取每页中帖子的ID
def getOnePageList(pn):
	url = "http://tieba.baidu.com/f"
	payload = {
	    'kw':'复仇者联盟',
	    'ie':'utf-8',
	    'tab':'good',
	    'pn':pn
	}
	try:
		response = requests.get(url, headers=header, params=payload, cookies=cookies)
		content = None

		if response.status_code == requests.codes.ok:
			content = response.text
			
	except Exception as e:
			print (e)

	pattern = re.compile('/p/(\d+)', re.S)
	data = pattern.findall(content)

	return data

# 获取每个帖子的内容，只看楼主
def getDetail(tid):
	url = "http://tieba.baidu.com/p/{0:s}".format(tid)
	payload = {
	    'see_lz':1
	}
	try:
		response = requests.get(url, headers=header, params=payload, cookies=cookies)
		content = None

		if response.status_code == requests.codes.ok:
			content = response.text
		else:
			return
			
	except Exception as e:
		print (e)

	soup = BeautifulSoup(content,'lxml')

	# 帖子不存在,但是请求的返回码是200
	print ("标题：" + soup.head.title.text)
	if soup.head.title.text == '贴吧404':
		print ("跳过。")
		return

	file = open("Download/{0:s}.txt".format(tid),'w',encoding = 'utf-8')
	
	file.write("Title: "+ soup.head.title.text + "\n")

	author = soup.find_all('div', class_='d_author')
	file.write("Author: " + author[0].img.get('username') + "\n")
	file.write("Avatar: " + author[0].img.get('src') + "\n")
	file.write("\n")

	# 获得页数
	pageCnt = soup.find('div', class_='pb_footer').find_all('span', class_='red')[1].text

	# 开始抓取所有的页数
	for i in range(1,int(pageCnt)+1):
		payload = {
	    	'see_lz':1,
	    	'pn':i
		}

		try:
			response = requests.get(url, headers=header, params=payload, cookies=cookies)
			content = None

			if response.status_code == requests.codes.ok:
				content = response.text
			
		except Exception as e:
			print (e)
			continue

		soup = BeautifulSoup(content,'lxml')
		details = soup.find_all('cc')

		for detail in details:
			file.write(detail.text.strip() + "\n")

			imgs = detail.find_all('img')
			if imgs:
				for img in imgs:
					file.write(img.get('src') + "\n")

			file.write("\n")

		time.sleep(0.25)

	file.close()
	print ("创建 {0:s}.txt 成功。".format(tid))


if __name__ == '__main__':
	cnt = getGoodCount()

	tidlist = []
	for i in range(0, cnt,50):
		tidlist += getOnePageList(i)
		time.sleep(0.25)

	print ("抓取到{0:d}个帖子。".format(len(tidlist)))

	for tid in tidlist:
		getDetail(tid)
