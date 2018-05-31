import requests
import ast
import json
from random import choice
from prettytable import PrettyTable
from colorama import init, Fore, Style


import Configure as Configs
import Sqlite3api as Sqlite3

init()

header = {}
header['user-agent'] = choice(Configs.FakeUserAgents)
header['Referer'] = "https://kyfw.12306.cn/otn/leftTicket/init"

def t12306_init():
	conn = Sqlite3.sqlite3_init()

	url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9053"
	content = None

	ret = Sqlite3.sqlite3_execute(conn, "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='t12306'")[0][0]
	if ret == 1:
		Sqlite3.sqlite3_execute(conn, "DROP TABLE t12306")

	Sqlite3.sqlite3_execute(conn, "CREATE TABLE t12306 (stationId real, stationName text, teleCode text, pinYin text, pinYinHead text)")
	Sqlite3.sqlite3_execute(conn, "CREATE UNIQUE INDEX idx_follow_stationId on t12306(stationId)")

	try:
		response = requests.get(url, headers=header)

		if response.status_code == requests.codes.ok:
			content = response.text
	except Exception as e:
		print (e)

	data = content[:-1].split('=')[1][2:]

	for station in data.split('@'):
		fields = station.split('|')
		Sqlite3.sqlite3_execute(conn, "INSERT INTO t12306 VALUES (?,?,?,?,?)", (fields[5],fields[1],fields[2],fields[3],fields[0],))
		#print (fields[5],fields[1],fields[2],fields[3],fields[0])
			
	Sqlite3.sqlite3_close(conn)


def check_left_ticket(train_date, from_station, to_station, purpose_codes, need_price=False):
	url = "https://kyfw.12306.cn/otn/leftTicket/query"

	payload = {
		'leftTicketDTO.train_date': train_date,
		'leftTicketDTO.from_station': from_station,
		'leftTicketDTO.to_station': to_station,
		'purpose_codes': purpose_codes
	}

	content = ''
	try:
		response = requests.get(url, headers=header, params=payload)
		if response.status_code == requests.codes.ok:
			response.encoding = 'utf-8'
			content = response.text
	except Exception as e:
		print (e)
	
	data = json.loads(content)
	#print (data)
	if data.get('status') == False:
		print ("获取数据失败。")
		return

	# 站点编号->站点名字 的Map
	name_map = data.get('data').get('map')

	table = PrettyTable()
	table.field_names = ["车次", "出发/到达", "出发/到达时间", "历时", "可否网购", "商务座", "特等座", "一等座", "二等座", "高级软卧", "软卧", "动卧", "硬卧", "软座","硬座", "无座", "其他"]
	table.align["车次"] = "l"
	table.align["出发/到达"] = "l"

	for ticket_list in data.get('data').get('result'):
		field = ticket_list.split('|')
		flag_id = "[身]" if field[18]=='1' else "" # 是否支持身份证
		flag_from = "[始]" if field[4] == field[6] else "[过]" # 是否始发站
		flag_to = "[终]" if field[5] == field[7] else "[过]"# 是否终点站

		price = {}
		if need_price == True:
			ret = query_ticket_price(field[2],field[16],field[17],field[35],train_date)
			price = ret if ret else {}

		table.add_row([
			field[3] + (Fore.YELLOW + flag_id + Fore.RESET ) ,
			'\n'.join([Fore.LIGHTGREEN_EX + flag_from + name_map.get(field[6]) + Fore.RESET,
						Fore.LIGHTRED_EX + flag_to + name_map.get(field[7]) + Fore.RESET]),
			'\n'.join([Fore.LIGHTGREEN_EX + field[8] + Fore.RESET,
						Fore.LIGHTRED_EX + field[9] + Fore.RESET]),
			field[10],
			"是" if field[10] else "否",
			# 商务座
			"{0:s}{1:s}".format(field[32] if field[32] else "--", ("\n" + Style.BRIGHT + price.get('A9')) + Style.RESET_ALL if price.get('A9') else ""),
			# 特等座
			"{0:s}{1:s}".format(field[25] if field[25] else "--", ("\n" + Style.BRIGHT + price.get('P')) + Style.RESET_ALL if price.get('P') else ""),
			# 一等座
			"{0:s}{1:s}".format(field[31] if field[31] else "--", ("\n" + Style.BRIGHT + price.get('M')) + Style.RESET_ALL if price.get('M') else ""),
			# 二等座 
			"{0:s}{1:s}".format(field[30] if field[30] else "--", ("\n" + Style.BRIGHT + price.get('O')) + Style.RESET_ALL if price.get('O') else ""),
			# 高级软卧
			"{0:s}{1:s}".format(field[21] if field[21] else "--", ("\n" + Style.BRIGHT + price.get('A6')) + Style.RESET_ALL if price.get('A6') else ""),
			# 软卧
			"{0:s}{1:s}".format(field[23] if field[23] else "--", ('\n' + Style.BRIGHT + price.get('A4')) + Style.RESET_ALL if price.get('A4') else ""),
			# 动卧
			field[33] if field[33] else "--",
			# 硬卧
			"{0:s}{1:s}".format(field[28] if field[28] else "--", ("\n" + Style.BRIGHT + price.get('A3')) + Style.RESET_ALL if price.get('A3') else ""),
			# 软座
			"{0:s}{1:s}".format(field[24] if field[24] else "--", ("\n" + Style.BRIGHT + price.get('A2')) + Style.RESET_ALL if price.get('A2') else ""),
			# 硬座
			"{0:s}{1:s}".format(field[29] if field[29] else "--", ("\n" + Style.BRIGHT + price.get('A1')) + Style.RESET_ALL if price.get('A1') else ""),
			# 无座
			"{0:s}{1:s}".format(field[26] if field[26] else "--", ("\n" + Style.BRIGHT + price.get('WZ')) + Style.RESET_ALL if price.get('WZ') else ""),
			# 其他
			field[22] if field[22] else "--"
			])
		
	print (table)

def query_ticket_price(train_no, from_station_no, to_station_no, seat_types, train_date):
	url = "https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice"

	#print (train_no, from_station_no, to_station_no, seat_types, train_date)
	payload = {
		'train_no': train_no,
		'from_station_no': from_station_no,
		'to_station_no': to_station_no,
		'seat_types': seat_types,
		'train_date': train_date,
	}

	try:
		response = requests.get(url, headers=header, params=payload)
		if response.status_code == requests.codes.ok:
			#response.encoding = 'utf-8'
			content = response.text
	except Exception as e:
		print (e)

	data = json.loads(content)

	if data.get('status') == False:
		print ("获取数据失败。")
		return None

	return data.get('data')


if __name__ == "__main__":
	#t12306_init()
	conn = Sqlite3.sqlite3_init()

	date = input("请输入乘车时间(YYYY-MM-DD): ")
	from_station = input("请输入出发车站: ")
	to_station = input("请输入到达车站: ")
	purpose_codes = input("请输入类型(1-成人票): ")
	from_s = to_s = ticket_type = None
	
	ret = Sqlite3.sqlite3_execute(conn, "SELECT teleCode FROM t12306 WHERE stationName ='{0:s}'".format(from_station))#[0][0]
	from_s = ret[0][0]

	ret = Sqlite3.sqlite3_execute(conn, "SELECT teleCode FROM t12306 WHERE stationName ='{0:s}'".format(to_station))#[0][0]
	to_s = ret[0][0]

	Sqlite3.sqlite3_close(conn)

	if purpose_codes == 1:
		ticket_type = 'ADULT'

	check_left_ticket(date, from_s, to_s, ticket_type, True)
	