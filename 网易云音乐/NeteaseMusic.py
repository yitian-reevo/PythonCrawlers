import requests
import re
import json
import os
import time
from random import choice
from prettytable import PrettyTable

import Configure
from Sqlite3api import * 
import DisplayResult as dr

url = "http://music.163.com/weapi/v3/playlist/detail"#?csrf_token=c471024dc44337a5c6a627ba90b47c6e"
header = {'user-agent': choice(Configure.FakeUserAgents)}
#payload = {'csrf_token':'c471024dc44337a5c6a627ba90b47c6e'}
formdata = {
	'params':'jBULGYRTVRVfR0k15G9wjIo43oTqF27KLw89P8drW6x1Igeb1tOuXVzTtI6VJi8n77nyaQN/es61paePKs0HDe3ILYLzH41xTWAzBGdnoS9k9onAr3lq9VpBXgW6n64cP64IXfB4rc5w+hmXP3TKnL7ZpKG5z/IbEVmZq5HbfAF7k6jBtXj3VATfWi4/9ZZxVY3qzm1F2/oEXKAtrlxUwghyRvOgkMonxMGtxZyFpJM=',
	'encSecKey':'51ffbd951e86680aaa5c274158822c79f677cf8c41afe815c7df29fcd811172f2587613d5cb9e6367f3032c980cf1d21f1a00fb357ebf62777a9d9babd8f73344155a60e366421725f0bab5da4f134e0a367c8e073e45711e71177243f584728e275563e0c42a1d66db731caf995e5cdb98a044abc871133f809e0eac0f204ae'
}
#cookies = {}

#cookiestr = '__f_=1524688672786; _ntes_nnid=db485c95c6901acef88e90d844e9720e,1524688669236; \
#				_ntes_nuid=db485c95c6901acef88e90d844e9720e; \
#				_iuqxldmzr_=32; \
#				__remember_me=true; \
#				__utmc=94650624; \
#				__utma=94650624.1055904552.1525039592.1525220980.1525224618.9; \
#				__utmz=94650624.1525224618.9.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); \
#				WM_TID=RRHt%2BF%2BgzZ6%2BbXWgT5BAA7qi%2BFPdLpNy; \
#				JSESSIONID-WYYY=bdQAAit65dBMPxeMu767ice6vEaq%2B%2BEYd24EDrz5p67FuZVNQFESJFY\
#					gygv%2BQjbIQyJrM4%5C6S3m3PkGF3hiB83n9Cki%2FpSMPRtdSxUQa5qZcBEBJPtvW2GtmpSDf\
#					QCdBU1suIorWHVpgdG4fllxpSxtrM6DBZuPBq9XVz749WwEtX2%2Bs%3A1525227547173; \
#				MUSIC_U=ba49f310c620d1f4e1ca78948278d9d8cadcc61448045996eb8693a4835a76a6c19\
#					a62ba5e2f5e641936fd7b8f93d102a70b41177f9edcea;\
#				__csrf=c1641a0a560d3d124a89f0edfd12517c; \
#				__utmb=94650624.26.10.1525224618'

#for cookie in cookiestr.split(';'):
#    name,value=cookie.strip().split('=',1)  
#    cookies[name]=value

# index
#res=requests.post(url, headers=header, params=payload, data=formdata, cookies=cookies)

def getSongList():
	try:	
		response = requests.post(url, headers=header, data=formdata)
		content = None

		if response.status_code == requests.codes.ok:
			content = response.text

	except RequestException as e:
		print (e)
		return


	lists = json.loads(content)
	tracks = lists.get('playlist').get('tracks')

	for track in tracks:
		#print (track)
		args = []
		args.append(track.get('id'))
		args.append(track.get('name'))
		args.append(int(track.get('l').get('size')) // int(track.get('l').get('br')) * 8)
		args.append(track.get('ar')[0].get('name'))
		args.append(track.get('al').get('name'))
		args.append('http://music.163.com/#/song?id={0:d}'.format(args[0]))
		args.append(0)
		
		sqlite3_execute("INSERT INTO info VALUES (?,?,?,?,?,?,?)", tuple(args))
		getSongDetail(args[0])
		#time.sleep(0.25)


def getSongDetail(id):
	url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{0:d}'.format(id)

	try:	
		response = requests.post(url, headers=header, data=formdata)
		content = None

		if response.status_code == requests.codes.ok:
			content = response.text

	except RequestException as e:
		print (e)
		return

	data = json.loads(content)

	CommentsCount = data.get('total')
	sqlite3_execute("UPDATE info SET comment = ? WHERE id = ?", (CommentsCount, id,))

	hotComments = data.get('hotComments')
	for hotComment in hotComments:
		user = hotComment.get('user').get('nickname')
		content = hotComment.get('content').strip().replace(' ','')
		sqlite3_execute("INSERT INTO comment VALUES (?,?,?)", (id, user, content,))



if __name__ == '__main__':
	sqlite3_init()

	#抓取数据，一般抓一次就好了
	sqlite3_execute("CREATE TABLE info (id int, name text, duration int, singer text, album text, songurl text, comment int)")
	sqlite3_execute("CREATE TABLE comment (id int, user text, comment text)")
	getSongList()
	

	# 展示数据
	#dr.DisplayResults()

	#sqlite3_execute("DROP TABLE info")
	#sqlite3_execute("DROP TABLE comment")

	sqlite3_close()

