import re
import Sqlite3api as sqlite3
import Configure as Configs
import requests
from random import choice
from bs4 import BeautifulSoup
import time
import ast

def import_data():
	with open('cityWeather18-03-4.sql', 'r', encoding='utf-8') as file:
		content = file.read()

	pattern = re.compile('(\d+),\'(.*?)\',\'(\d+)\'',re.S)
	data = pattern.findall(content)
	print ("Retrieve {0:d} weather codes.".format(len(data)))

	conn = sqlite3.sqlite3_init()

	for d in data:
		print (d)
		sql = "INSERT INTO weather VALUES ({0:s},'{1:s}',{2:s})".format(d[0], d[1].strip(),d[2])
		sqlite3.sqlite3_execute(conn, sql)

	sqlite3.sqlite3_close(conn)

def get_citycode_by_cityname(cityname):
	conn = sqlite3.sqlite3_init()

	ret = sqlite3.sqlite3_execute(conn, "select cityname, citycode from weather WHERE cityname LIKE '%{0:s}%'".format(cityname))

	sqlite3.sqlite3_close(conn)

	return ret

def get_weather_by_citycode(citycode):
	url = "http://d1.weather.com.cn/sk_2d/{0:d}.html?_={1:d}".format(citycode, int(time.time()*1000))

	header = {}
	header['user-agent'] = choice(Configs.FakeUserAgents)
	header['Referer'] = "http://www.weather.com.cn/weather1d/101190101.shtml"

	try:
		response = requests.get(url, headers=header)
		content = ''
		if response.status_code == requests.codes.ok:
			response.encoding = 'utf-8'
			content = response.text
	except Exception as e:
		print (e)

	pattern = re.compile('{(.*?)}', re.S)
	data = pattern.findall(content)[0]
	data = ast.literal_eval("{"+data+"}")

	print ("城市:", data.get('cityname'))
	print ("日期:", data.get('date'))
	print ("时间:", data.get('time'))
	print ("摄氏温度:", data.get('temp'))
	print ("华氏温度:", data.get('tempf'))
	print ("天气:", data.get('weather'))
	print ("湿度:", data.get('SD'))
	print ("风向:", data.get('WD'))
	print ("风级:", data.get('WS'))
	print ("空气质量:", data.get('aqi'))
	print ("空气质量PM2.5:", data.get('aqi_pm25'))



def main():
	while True:
		print ("-"*80)
		cityname = input("请输入要查询的城市名: ")

		ret = get_citycode_by_cityname(cityname)

		if not ret:
			print ("没有找到该城市，请重新输入。")
			continue
		
		if 1 == len(ret):
			get_weather_by_citycode(int(ret[0][1]))
			continue

		cnt = 1
		table = PrettyTable()
		table.field_names = ["编号", "城市名字"]
		table.sortby = "编号"

		for r in ret:
			table.add_row([cnt, r[0]])
			cnt += 1

		print (table)

		code = int(input("找到不只一个城市，请输入其编号: "))
		get_weather_by_citycode(int(ret[code-1][1]))
	


if __name__ == '__main__':
	#import_data()
	main()
	