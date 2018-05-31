 import requests
import re
import json
import os
import time
from random import choice
import random
import execjs

from js import jsstr
import Configure

url = "https://www.xiami.com/playercollect/list"
header = {'user-agent': choice(Configure.FakeUserAgents)}

cookies = {}

cookiestr = '''gid=152425845220935; 
			_unsign_token=1ce1fe55087ea1f21db47780701aa248; 
			cna=BOBeExJaZ2MCAUWMrkuEudTQ; 
			UM_distinctid=162e4e236948cf-0773ed2704ac51-3b60490d-1fa400-162e4e236957a6; 
			join_from=0zqfTI9Kv2Ew3f7BEdw; 
			_xiamitoken=9934bc4572854b88e3b35017a976a3c7; 
			user_from=2; 
			PHPSESSID=abdb66f05f100adc171436cdc0db744a; 
			s_uid=2523264732; 
			access_token=2.00Q73lkC81ERME01ffcdd5d907MPnY; 
			__XIAMI_SESSID=9dd80406b67dc4af1df541f343f5ecdf; 
			xmgid=6539bf5e-7321-44d3-ab3d-0d8ff66d0f50; 
			connect_sina=76633; 
			expires_in=2652725; 
			CNZZDATA2629111=cnzz_eid%3D1724500643-1524255732-https%253A%252F%252Fwww.google.com%252F%26ntime%3D1525313285; 
			_umdata=535523100CBE37C33075D564A95D152BC5B96D713321CA2CED3D987F95DDB172352CD465FA09B190CD43AD3E795C914C6D829DD7915A193EB257667C30CCA2E2; 
			member_auth=hWrNTo4duj9lgqPAT4FlIiIW4OLdHDLSwo0C3rIl5AMhJ9wBa4TxlauSRAlB3SiVqVEmwDAiBbv9xkT9%2FlYdtts; 
			user=362958619%22%E4%BD%8E%E8%B0%83%E9%9A%90%E5%BF%8DOB%22%220%220%22do%220%220%220%22975ef99c85%221525314365; 
			t_sign_auth=0; 
			CNZZDATA921634=cnzz_eid%3D1878118879-1524256440-https%253A%252F%252Fwww.google.com%252F%26ntime%3D1525314514; 
			form_timestamp=1525318171; 
			XMPLAYER_url=/song/playlist-default; 
			XMPLAYER_addSongsToggler=0; 
			__guestplay=MTc3NDMyMTIxNSw2OzE3OTYwMzI0MTMsMjA7MTgwMzAwMjM4MSw0OzE3OTYwMzI0MTIsMg%3D%3D; 
			XMPLAYER_isOpen=0; 
			isg=BEREMy-7wt1ZiXahWEFx4c_eFcI8XWhO-TQFnl7k1I_SieVThG1fVPBozTdRyqAf
			'''

for cookie in cookiestr.split(';'):
    name,value=cookie.strip().split('=',1)  
    cookies[name]=value

def getRandomParams():
	a = int(time.time()*1000)
	b = random.randint(200,1000)

	return {'_ksTS':'{0:d}_{1:d}'.format(a,b), 'callback':'jsonp{0:d}'.format(b+1)}

def getPlaylist():
	playlist = []
	try:	
		response = requests.get(url, headers=header, params=getRandomParams(), cookies=cookies)
		content = None

		if response.status_code == requests.codes.ok:
			content = response.text
			
	except Exception as e:
		print (e)

	pattern = re.compile('"list_id":(\d+),', re.S)
	data = pattern.findall(content)
	return data

def getSongLocation(list_id):

	url2 = "https://www.xiami.com/song/playlist/id/{0:s}/type/3/cat/json".format(list_id)

	header = {}
	header['user-agent'] =  choice(Configure.FakeUserAgents)
	header['referer'] = 'https://www.xiami.com/play?ids=/song/playlist/id/1796032423/object_name/default/object_id/0'

	payload = {
		'_ksTS':'{0:d}_428'.format(int(time.time()*1000)), 
		'callback':'jsonp_429'
	}

	try:	
		response = requests.get(url2, headers=header, params=payload, cookies=cookies)
		content = None
		
		if response.status_code == requests.codes.ok:
			content = response.text
			
	except Exception as e:
		print (e)
	
	data = json.loads(content[11:][:-1])
	tracklists = data.get('data').get('trackList')
	ctx = execjs.compile(jsstr)

	res = []
	for track in tracklists:
		tmp = {}
		tmp['songName'] = track.get('songName')
		tmp['singers'] = track.get('singers')
		tmp['location'] = "http:"+ ctx.call('getLocation',  track.get('location'))
		res.append(tmp)

	return res

def DownloadSong(SongURLs):
	if not os.path.exists("Download"):
		os.makedirs("Download")

	for songurl in SongURLs:
		req = requests.get(songurl.get('location'))
		filename = "{0:s}-{1:s}.mp3".format(songurl.get('songName'), songurl.get('singers'))
		with open("Download/"+filename, 'wb') as file:    
		    file.write(req.content)
		print ("Download {0:s} Successfully.".format(filename))	


if __name__ == '__main__':
	ids = getPlaylist()
	for list_id in ids:
		res = getSongLocation(list_id)
		DownloadSong(res)
		