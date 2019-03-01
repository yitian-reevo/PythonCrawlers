"""
lagou的爬取（2019.3.1可用）
主要的trick其实是拉钩会在每次搜索前先下发一个SEARCH_ID，因此需要先访问init_url一次获取这个id，当然还有一些其他字段，见代码。
"""
import requests
keyword = 'Python'
init_url = 'https://www.lagou.com/jobs/list_{}?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='.format(keyword)
url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'Referer': 'https://www.lagou.com/jobs/list_Python?labelWords=&fromSearch=true&suginput=',
    'Host': 'www.lagou.com'
}
formdata = {
    'first': 'true',
    'pn': 1,
    'kd': keyword
}

resp = requests.get(init_url, headers=headers, timeout=10)
print(resp.cookies.get_dict())
search_id = resp.cookies.get('SEARCH_ID')
lgr_id = resp.cookies.get('LGRID')
jession_id = resp.cookies.get('JSESSIONID')
print('Get new SEARCH_ID: {}, LGRID: {}, JSESSIONID: {}'.format(search_id, lgr_id, jession_id))

if search_id and lgr_id and jession_id:
    headers['Cookie'] = 'JSESSIONID={}; user_trace_token={}; LGSID={}; LGUID={}; LGRID={}; SEARCH_ID={}'.format(
        jession_id, lgr_id, lgr_id, lgr_id, lgr_id, search_id)
    resp = requests.post(url, headers=headers, data=formdata, timeout=10).json()
    print(resp)
else:
    print('exception.')
