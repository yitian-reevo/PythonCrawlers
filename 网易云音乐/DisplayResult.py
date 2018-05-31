from prettytable import PrettyTable
from prettytable import ALL
from prettytable import FRAME
from prettytable import NONE
import os
import re
from Sqlite3api import * 

def DisplayResults():
	table = PrettyTable()
	table.field_names = ["ID", "音乐标题", "时长", "歌手", "专辑", "评论数"]
	table.sortby = "评论数"
	table.reversesort=True
	
	page = 12
	offset = 12
	data = sqlite3_execute("SELECT id, name, duration, singer, album, comment FROM info limit {0:d}".format(page))

	for item in data:
		l = list(item)
		l[2] = "{0:d}:{1:02d}".format(l[2]//60,l[2] - l[2]//60*60)
		table.add_row(l)  

	print (table)

	patterns = []
	patterns.append(re.compile('show (\d+)', re.S))
	patterns.append(re.compile('showrange (\d+),(\d+)', re.S))
	patterns.append(re.compile('set page (\d+)', re.S))
	patterns.append(re.compile('comment (\d+)', re.S))
	patterns.append(re.compile('quit', re.S))
	patterns.append(re.compile('help', re.S))
	patterns.append(re.compile('next', re.S))

	while True:
		inputstr = input("输入命令:")
		data = None
		idx = None
		for pattern in patterns:
			data = pattern.findall(inputstr)
			if data:
				idx = patterns.index(pattern)
				break
		# show ID
		if 0 == idx:
			table = PrettyTable()
			table.field_names = ["ID", "音乐标题", "时长", "歌手", "专辑", "评论数"]

			data = sqlite3_execute("SELECT id, name, duration, singer, album, comment FROM info WHERE id={0:d}".format(int(data[0])))

			if data:
				for item in data:
					l = list(item)
					l[2] = "{0:d}:{1:02d}".format(l[2]//60,l[2] - l[2]//60*60)
					table.add_row(l)

			print (table)
		# showrange #1,#2
		elif 1 == idx:
			table = PrettyTable()
			table.field_names = ["ID", "音乐标题", "时长", "歌手", "专辑", "评论数"]
			table.sortby = "评论数"
			table.reversesort=True
			data = sqlite3_execute("SELECT id, name, duration, singer, album, comment FROM info LIMIT {0:d} OFFSET {1:d}".format(int(data[0][1]) - int(data[0][0]),int(data[0][0])))

			if data:
				for item in data:
					l = list(item)
					l[2] = "{0:d}:{1:02d}".format(l[2]//60,l[2] - l[2]//60*60)
					table.add_row(l)

			print (table)
		# set page #
		elif 2 == idx:
			page = int(data[0])
		# comment #
		elif 3 == idx:
			table = PrettyTable()
			table.field_names = ["评论内容","用户"]
			table.align["评论内容"] = "l" 
			table.hrules = ALL
			data = sqlite3_execute("SELECT comment, user FROM comment WHERE id={0:d}".format(int(data[0])))

			if data:
				for item in data:
					table.add_row(list(item))

			print (table)
		# quit
		elif 4 == idx:
			os._exit(0)
		# help 
		elif 5 == idx:
			print ("                    命令列表:")
			print ("    next                    --- 打印下一页歌曲")
			print ("    show _id_               --- 打印ID为id的歌曲")
			print ("    showrange _begin_,_end_ --- 打印从begin到end的歌曲 ")
			print ("    set page _num_          --- 设置每页的歌曲数 ")
			print ("    comment _id_            --- 打印ID为id的歌曲的热门评论 ")
			print ("    help                    --- 打印本列表")
			print ("    quit                    --- 退出程序")
		# next
		elif 6 == idx:
				table = PrettyTable()
				table.field_names = ["ID", "音乐标题", "时长", "歌手", "专辑", "评论数"]
				table.sortby = "评论数"
				table.reversesort=True
				data = sqlite3_execute("SELECT id, name, duration, singer, album, comment FROM info LIMIT {0:d} OFFSET {1:d}".format(page, offset))
				offset += page
				for item in data:
					l = list(item)
					l[2] = "{0:d}:{1:02d}".format(l[2]//60,l[2] - l[2]//60*60)
					table.add_row(l)  

				print (table)
		else:
			print ("非法的指令")

if __name__ == '__main__':
	sqlite3_init()

	DisplayResults()
		
	sqlite3_close()
