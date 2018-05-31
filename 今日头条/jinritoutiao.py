import requests
import json
import time
import re
from random import choice
import configure

url = "https://www.toutiao.com/search_content/?"
header = {'user-agent': choice(configure.FakeUserAgents)}
keyword = '塞尔达传说'

has_gallery_lists = []
no_gallery_lists = []

def SearchPageParser(offset = 0):
	payload = {
		'offset':offset,
		'format':'json',
		'keyword':keyword,
		'autoload':'true',
		'count':30,
		'cur_tab':1,
		'from':'search_tab'
	}

	count = 0

	try:	
		response = requests.get(url, headers=header, params=payload)
		content = None

		print ("Parser " + response.url)
		if response.status_code == requests.codes.ok:
			content = response.text
			data = json.loads(content)

			if not data:
				return

			for article in data.get('data'):
				if True == article.get('has_gallery') and True == article.get('has_image'):
					has_gallery_lists.append(article.get('article_url'))
					count += 1

				if False == article.get('has_gallery') and True == article.get('has_image'):
					no_gallery_lists.append(article.get('article_url'))
					count += 1

			return count	

	except Exception as e:
		print (e)
		return

def SaveImage(imageURL):
	# 这里就不下载了，只是把单纯写入文件
	print (imageURL)

	with open('toutiao.txt', 'a') as file:
		file.write(imageURL + '\n')


def HasGalleryParser():
	if 0 == len(has_gallery_lists):
		return

	# 这里写的时候注意(, ), ", ., 都是要转义的。
	pattern = re.compile('gallery: JSON\.parse\("(.*?)max_img', re.S)

	while has_gallery_lists:
		this = has_gallery_lists.pop()

		try:	
			response = requests.get(this, headers=header)
			content = None

			if response.status_code == requests.codes.ok:
				content = response.text
				data = pattern.findall(content)

				if data:
					data = data[0][:-4].replace('\\','') + ']}'
					img_urls = json.loads(data).get('sub_images')

					for img_url in img_urls: 
						SaveImage(img_url.get('url'))
				else:
					print ("BadPageURL[GalleryParser, {0:s}]".format(this))

		except Exception as e:
			print (e)
			return

	time.sleep(0.25)

def NoGalleryParser():
	if 0 == len(no_gallery_lists):
		return

	while no_gallery_lists:
		this = no_gallery_lists.pop()

		pattern = re.compile('&lt;img src&#x3D;&quot;(.*?)&quot;', re.S)
		try:	
			response = requests.get(this, headers=header)
			content = None

			if response.status_code == requests.codes.ok:
				content = response.text
				img_urls = pattern.findall(content)
				
				if img_urls:
					for img_url in img_urls: 
						SaveImage(img_url)
				else:
					print ("BadPageURL[NoGalleryParser, {0:s}]".format(this))

		except Exception as e:
			print (e)
			return

	time.sleep(0.25)



if __name__ == "__main__":
	x, count = 0, 0

	cnt_urls = SearchPageParser(x)

	while count < 20 and cnt_urls:
		cnt_urls = SearchPageParser(x+20)
		count += cnt_urls
		x += 20
		time.sleep(0.55)

	print ("Get {0:d} URL(s) in total.".format(count))

	HasGalleryParser()
	NoGalleryParser()