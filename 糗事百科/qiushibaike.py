# Standard Lib
import urllib
import hashlib
import time
from urllib import request
from urllib import error
from bs4 import BeautifulSoup
from random import choice

# User Lib
import db
import ui
import configure

# 这里几个标签的URL都可以爬，因为结构都是一样的
# 依次是热门，24小时，热图，文字，穿越，糗图，新鲜
TargetURLs = ['https://www.qiushibaike.com/',
			'https://www.qiushibaike.com/imgrank/',
			'https://www.qiushibaike.com/hot/',
			'https://www.qiushibaike.com/text/',
			'https://www.qiushibaike.com/history/',
			'https://www.qiushibaike.com/pic/',
			'https://www.qiushibaike.com/textnew/'
		]

Domain = 'https://www.qiushibaike.com'

def OnepageSpider(myTargetURL = choice(TargetURLs)):
	print ("Start to spider: {0:s}".format(myTargetURL))
	try:
		# 构建请求
		req = request.Request(myTargetURL)
		req.add_header("User-Agent",choice(configure.FakeUserAgents))
		response = request.urlopen(req)
		if response.getcode() != 200:
			print ("HTTP Request Code: {0:d}".format(response.getcode()))
			return myTargetURL, 0
		html = response.read()
	except error.URLError as e:
		if hasattr(e,"code"):
			print(e.code)
		if hasattr(e,"reason"):
			print(e.reason)

	# 用bs4解析
	soup = BeautifulSoup(html, 'lxml')

	# 这里有时候会失败，但是再试一次就能成功，所以加个判断
	# 失败的原因没找到，初步断定不是网络波动
	# 可能和css选择器的表达式有关
	if soup.select('div.col1'): 
		results = soup.select('div.col1')[0].select("div.article")
	else:
		print ("SOMETHING IS WRONG, TRY AGAIN LATER.")
		return myTargetURL, 0

	# 解析数据并写入DB
	count = 0
	for res in results:
		# 首先解析URL，判断是否已经在数据库里
		url = Domain + res.find_all('a', class_='contentHerf')[0].get('href')
		# md5
		m = hashlib.md5()
		m.update(url.encode('utf-8'))
		url_md5 = m.hexdigest()
		
		if db.DuplicationCheck(url_md5):
			continue

		# 不在数据库里，继续解析其他值
		author = res.find('h2').get_text().strip()
		
		stat = res.find_all('i', class_='number')
		
		# 如果评论数是0，就会不显示
		# 我暂时没找到好笑数是0的帖子，不过也这样写了
		if len(stat) == 0:
			fun, comment = 0
		elif len(stat) == 1:
			fun = stat[0].get_text()
			comment = 0
		else:
			fun = stat[0].get_text()
			comment = stat[1].get_text()

		content = res.select("div.content span")[0].get_text().strip()

		if res.select("div.thumb"):
			img_urls = "https:" + res.select("div.thumb img")[0].get('src')
		else:
			img_urls = None


		if True == db.DBupdate(url, url_md5, author, int(fun), int(comment), content, img_urls):
			count += 1

	
	# 解析下一页的URL，并返回这个URL
	next = soup.select('div.col1 ul.pagination li')[-1].a
	# 这个地方这么写，是因为有的页面最后一页是个“更多”的标签，而有的是空的
	# 为了适配所有页面的抓取，要多加一个判断
	if next and next.span.get_text().strip() == '下一页':
		next_url = Domain + next.get('href')
	else:
		next_url = None

	return next_url, count

# 从URL里找一个抓一轮
# 就是一直抓到没有下一页为止，一般是13页，有一个页面是25页
def OneCircleSpider():
	total = 0

	next_url, num = OnepageSpider()
	print ("Spider One Page. Add {0:d} record(s)".format(num))
	total += num
	
	while next_url:
		next_url, num = OnepageSpider(next_url)
		total += num
		print ("Spider One Page. Add {0:d} record(s)".format(num))
		time.sleep(1)
	
	print ("Add {0:d} record(s) in this circle".format(total))
	
	return total

def main():
	db.DBconnect()
	ui.init_ui()
	db.DBclose()
	
if __name__ == '__main__':
	main()