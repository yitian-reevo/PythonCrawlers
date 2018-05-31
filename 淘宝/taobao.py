import requests
import re
import json
import time
from random import choice
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from selenium import webdriver

import Configure

header = {}
header['user-agent'] =  choice(Configure.FakeUserAgents)
header['referer'] = 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm'

cookies = {}
cookiestr = '''
			v=0;cna=dqR1EyoV130CAUWMrkt9ktmY;cookie2=104577c67543527680bce385564c9ab8;tracknick=hyt272129018;_tb_token_=353a7843eba93;t=f818d399605188bdb688efe4f8a26f27;uc3=nk2=CzSiq1YmG4ftuXij&id2=VWoikG%2BL84R9&vt3=F8dBz44mnM5dx1ClHBE%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D;existShop=MTUyNTU5MzcyOA%3D%3D;lgc=hyt272129018;mt=ci=1_1;dnk=hyt272129018;sg=815;csg=de9f644f;cookie1=AnIpR6rpW91bz28Dpe4wT6OKuXiTQjgQv8AjnnCHmNo%3D;unb=653837081;skt=c3867ea588a18a29;publishItemObj=Ng%3D%3D;_cc_=Vq8l%2BKCLiw%3D%3D;tg=0;_l_g_=Ug%3D%3D;_nk_=hyt272129018;cookie17=VWoikG%2BL84R9;thw=us;_m_h5_tk=d65b45db04c04dfad804a1cc80ded471_1525595891724;_m_h5_tk_enc=912a6301defc0a77b00fbcf6d5dd13a6;isg=BG9vPdaQaQj77m00x0tyxgKC_oNzFMO_-1dHwoH8FV7l0I_SieRThm0CVtdu85uu;uc1=cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie21=UtASsssme%2BBq&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoTeO8hnrWEm7w%3D%3D&tag=8&lng=zh_CN
			'''

for cookie in cookiestr.split(';'):
    name,value=cookie.strip().split('=',1)  
    cookies[name]=value

def getOnePageOrderHistory(pageNum, newURL=None):
	url = "https://buyertrade.taobao.com/trade/itemlist/asyncBought.htm"
	payload = {
		'action':'itemlist/BoughtQueryAction',
		'event_submit_do_query':1,
		'_input_charset':'utf8'
	}
	formdata = {
		'pageNum':pageNum,
		'pageSize':15,
		'prePageNo':pageNum-1
	}

	# 验证码通过后，新的URL后面会带Token值
	# 带着这个值才能访问成功，并且访问下个页面不再需要验证码
	# newURL就是通过验证后的新URL
	if newURL:
		url = newURL

	try:
		response = requests.post(url, headers=header, params=payload, data=formdata, cookies=cookies)
		content = None

		if response.status_code == requests.codes.ok:
			content = response.text
			
	except Exception as e:
			print (e)

	# 成功直接获取订单，失败进入验证码流程
	data = json.loads(content)
	if data.get('mainOrders'):
		getOrderDetails(data.get('mainOrders'))
	else:
		passCodeCheck(data.get('url'), pageNum)

# 打印订单信息
def getOrderDetails(data):
	table = PrettyTable()
	table.field_names = ["ID", "卖家", "名称", "订单创建时间", "价格", "状态"]

	for order in data:
		tmp = []
		#id = 
		tmp.append(order.get('id'))
		#shopName
		tmp.append(order.get('seller').get('shopName'))
		#title
		tmp.append(order.get('subOrders')[0].get('itemInfo').get('title'))
		#createTime
		tmp.append(order.get('orderInfo').get('createTime'))
		#actualFee
		tmp.append(order.get('payInfo').get('actualFee'))
		#text
		tmp.append(order.get('statusInfo').get('text'))

		table.add_row(tmp)

	print (table)

def passCodeCheck(referer_url, pageNum):
	# 在url中插入style=mini获取包含后续要用到的所有参数的页面
	url = referer_url.replace("?", "?style=mini&")

	try:
		response = requests.post(url, headers=header, cookies=cookies)
		content = None

		if response.status_code == requests.codes.ok:
			content = response.text
			
	except Exception as e:
		print (e)

	# 获取identity, sessionid和type
	pattern = re.compile(
		'new Checkcode\({.*?identity: \'(.*?)\''
		'.*?sessionid: \'(.*?)\''
		'.*?type: \'(.*?)\'.*?}\)', re.S)
	data = pattern.findall(content)
	
	m_identity = data[0][0]
	m_sessionid = data[0][1]
	m_type = data[0][2]

	# 获取action, m_event_submit_do_unique, m_smPolicy
	# m_smApp, m_smReturn, m_smCharset, smTag
	# captcha和smSign
	pattern = re.compile(
		'data: {'
		'.*?action: \'(.*?)\''
		'.*?event_submit_do_unique: \'(.*?)\''
		'.*?smPolicy: \'(.*?)\''
		'.*?smApp: \'(.*?)\''
		'.*?smReturn: \'(.*?)\''
		'.*?smCharset: \'(.*?)\''
		'.*?smTag: \'(.*?)\''
		'.*?captcha: \'(.*?)\''
		'.*?smSign: \'(.*?)\',', re.S)
	data = pattern.findall(content)
	
	m_action = data[0][0]
	m_event_submit_do_unique = data[0][1]
	m_smPolicy = data[0][2]
	m_smApp = data[0][3]
	m_smReturn = data[0][4]
	m_smCharset = data[0][5]
	m_smTag = data[0][6]
	m_captcha = data[0][7]
	m_smSign = data[0][8]

	# 处理验证码
	res = False
	m_code = ""
	while res == False:
		res, m_code = checkCode(m_identity, m_sessionid, m_type, url)

	# 构建URL，获取最后的Token
	murl = "https://sec.taobao.com/query.htm"

	mheader = {}
	mheader['user-agent'] =  choice(Configure.FakeUserAgents)
	mheader['referer'] = url

	mpayload = {
		'action':m_action,
		'event_submit_do_unique':m_event_submit_do_unique,
		'smPolicy':m_smPolicy,
		'smApp':m_smApp,
		'smReturn':m_smReturn,
		'smCharset':m_smCharset,
		'smTag':m_smTag,
		'captcha':m_captcha,
		'smSign':m_smSign,
		'ua':getUA(), # 获取最新的UA
		'identity':m_identity,
		'code':m_code,
		'_ksTS':'{0:d}_39'.format(int(time.time()*1000)),
		'callback':'jsonp40'
	}

	try:
		response = requests.get(murl, headers=mheader, params=mpayload, cookies=cookies)
		content = None
		
		if response.status_code == requests.codes.ok:
			content = response.text
			
	except Exception as e:
		print (e)

	pattern = re.compile('{(.*?)}', re.S)
	data = pattern.findall(content)
	jsond = json.loads('{'+data[0]+'}')

	# 这个json文件里包含了最后访问用的URL
	murl = jsond.get('url')
	getOnePageOrderHistory(pageNum, murl)


def checkCode(m_identity, m_sessionid, m_type, url):
	# 获取验证码的图片
	murl = "https://pin.aliyun.com/get_img"

	mheader = {}
	mheader['user-agent'] =  choice(Configure.FakeUserAgents)
	mheader['referer'] = url

	mpayload = {
		'identity':m_identity,
		'sessionid':m_sessionid,
		'type':m_type,
		't':int(time.time()*1000)
	}

	try:
		response = requests.get(murl, headers=mheader, params=mpayload, cookies=cookies)
		content = None
		
		if response.status_code == requests.codes.ok:
			content = response.content
			
	except Exception as e:
		print (e)

	# 将验证码图片写入本地
	with open("codeimg.jpg","wb") as file:
		file.write(content)

	# 输入并验证验证码
	code = input("请输入验证码：")

	murl = "https://pin.aliyun.com/check_img"

	mpayload = {
		'identity':m_identity,
		'sessionid':m_sessionid,
		'type':m_type,
		'code':code,
		'_ksTS': '{0:d}_29'.format(int(time.time()*1000)),
		'callback':'jsonp30',
		'delflag':0
	}

	try:
		response = requests.get(murl, headers=mheader, params=mpayload, cookies=cookies)
		content = None
		
		if response.status_code == requests.codes.ok:
			content = response.text
			
	except Exception as e:
		print (e)

	# 检测是否成功
	# 这里要返回这个验证码，后面会用到
	pattern = re.compile("SUCCESS",re.S)
	data = pattern.findall(content)

	if data:
		return True, code
	else:
		return False, code

def getUA():
	# 利用PhantomJS模拟浏览器行为
	# 访问本地的js文件来获取UA
	driver = webdriver.PhantomJS()
	driver.get("file:///D:/OneDrive/Documents/Python%E5%92%8C%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/code/taobao/ua.html")
	content = driver.find_element_by_tag_name('p').text
	driver.close()

	return content
	

if __name__ == '__main__':
	for i in range(2,25):
		getOnePageOrderHistory(i)
		print ("抓取第{0:d}页。".format(i))
		time.sleep(2)