import requests,time,random,string,hashlib
from url import *
from config import *

# -------  加密算法 --------#
#生成MD5
def md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()

#生成指定位数随机字符串
def randomStr(n):
    return (''.join(random.sample(string.ascii_lowercase, n))).upper()

#老ds算法函数 
def getlDS():
    n = 'cx2y9z9a29tfqvr1qsq6c7yz99b5jsqt'
    i = str(int(time.time()))
    r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
    c = md5("salt=" + n + "&t=" + i + "&r=" + r)
    return "{},{},{}".format(i, r, c)

#ds算法函数 
def getDS():
    n = "fd3ykrh7o1j54g581upo1tvpam0dsgtf"
    i = str(int(time.time()))
    r = randomStr(6)
    c = md5("salt=" + n + "&t=" + i + "&r=" + r)
    return "{},{},{}".format(i, r, c)

# -------  请求头函数  --------#
#原神奖励请求头
def YsRewardHead():
	head = {
		'User-Agent':'Mozilla/5.0 (Linux; Android 7.0; Meizu S6 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.110 Mobile Safari/537.36 miHoYoBBS/2.2.0',
		'x-rpc-device_id':'2eee2fdb-0cc1-3f25-8e5c-0e2b06439cbd',
		'referer':'https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required=true&act_id=e202009291139501&utm_source=bbs&utm_medium=mys&utm_campaign=icon',
		'x-rpc-app_version':'2.2.1',
		'Host':'api-takumi.mihoyo.com',
		'x-rpc-client_type':'5',
		'Content-Type':'application/json;charset=UTF-8',
		'Accept':'application/json, text/plain, */*',
		'cookie':YsRewardCookie,
		'X-Requested-With':'com.mihoyo.hyperion',
		'ds':getlDS()
	}
	return head

#原神bbs头函数
def mihoyo_bbs_head():
	headers = {
		'DS':getDS(),
		'cookie':mihoyo_bbs,
		'x-rpc-client_type':'2',
		'x-rpc-app_version':app_version,
		'x-rpc-sys_version':'12',
		'x-rpc-device_id':'818b3153-e80a-3697-81db-f96cc9c693de',
		'x-rpc-channel':'xiaomi',
		'x-rpc-device_name':'Xiaomi M2012K11AC',
		'x-rpc-device_model':'M2012K11AC',
		'host':'bbs-api.mihoyo.com',
		'referer':'https://app.mihoyo.com'

	}
	return headers

# -------  米游社bbs模块  --------#
#论坛签到函数
def bbs_sign():
	if mihoyo_bbs == "":
		print('没有论坛cookie，跳过执行。')
		return '论坛签到结果: 没有配置论坛cookie'
	else:
		for i in gameList:
			zz = requests.post(url=plate_signin_url.format(i["id"]),headers=mihoyo_bbs_head()).json()
			if zz['message'] == 'OK':
				print('签到结果：{}-签到成功'.format(i["name"]))
			else:
				print('签到结果：'+ i["name"] + "-" + str(zz['message']))
		return '论坛签到结果：' + zz['message']

#获取帖子id
def getpost():
	post_id = []
	dzysj = requests.get(url=post_url).json()
	for x in dzysj['data']['list']:
		post_id.append(x['post']['post_id'])
	return post_id

#分享贴子
def share(post_id):
	zz = requests.get(url=share_url.format(post_id[0]),headers=mihoyo_bbs_head()).json()
	if zz['message'] == 'OK':
		return "分享帖子：成功"
	else:
		return "分享帖子：失败"

#看贴
def latsk(post_id):
	for i in range(3):
		zz = requests.get(see_post_url.format(post_id[i]),headers=mihoyo_bbs_head()).json()
		if zz['message'] == 'OK':
			print('看贴成功')
		else:
			print('看贴失败')
	return "看贴："+zz['message']

#米游社帖子点赞/看贴/分享
def mysdz(post_id):
	if mihoyo_bbs == "":
		print('没有论坛cookie，跳过执行。')
		return '论坛签到结果: 没有配置论坛cookie'
	else:
		for x in range(0,5):
			postid = post_id[x]
			data = '{"is_cancel":false,"post_id":"'+ postid +'"}'
			dafh = requests.post(url=Like_url,data=data,headers=mihoyo_bbs_head()).json()
			print(dafh['message'])
		return "{}\n{}\n{}\n".format(dafh['message'],latsk(post_id),share(post_id))

# -------  原神签到奖励模块  --------#
#获取今日奖励信息函数
def getjlxx(sj):
	zz = requests.get(url=Todays_reward_url,headers=YsRewardHead()).json()
	sy = int(sj)
	return '今日奖励: ' + zz["data"]['awards'][sy]['name'] + ' x ' + str(zz["data"]['awards'][sy]['cnt'])

#获取游戏uid函数
def qsj():
	zz = requests.get(url=get_Game_uid,headers=YsRewardHead()).json()
	return zz['data']['list'][0]

#获取累计签到函数
def zsj(qsj):
	print(qsj['region'])
	url = get_Cumulative_check_in_url.format(qsj['region'],'e202009291139501',qsj['game_uid'])
	zz = requests.get(url=url,headers=YsRewardHead()).json()
	return zz['data']['total_sign_day']

#游戏每日签到函数
def yxqd(qsj):
	data = '{"act_id":"e202009291139501","region":"'+ qsj['region'] +'","uid":"'+ qsj['game_uid'] +'"}'
	zz = requests.post(url=Check_in_daily_url,data=data,headers=YsRewardHead()).json()
	if zz['message'] == 'OK':
		return '签到结果: 签到完成'
	else:		
		return '签到结果: ' + zz['message']

#微信积分签到函数
def wxqd():
	if wxqd_cookie == "":
		return "微信积分商城：cookie没有配置"
	elif wxqd_token == "":
		return "微信积分商城：token没有配置"
	else:
		head = {
			'User-Agent':'Mozilla/5.0 (Linux; Android 12; M2012K11AC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36 MMWEBID/3668 MicroMessenger/8.0.16.2040(0x28001055) Process/tools WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
			'Origin':"http://ysjfsc.mihoyo.com",
			'Referer':"http://ysjfsc.mihoyo.com/mobile/user/userinfo",
			'Cookie':wxqd_cookie
		}
		zz = requests.post(url=wxqd_url,data=wxqd_token,headers=head).json()
		if zz["ok"] == 1:
			return "微信积分商城：签到成功，积分+{}".format(zz["msg"])
		else:
			return "微信积分商城：签到失败，{}".format(zz["msg"])

# -------  运行模块  --------#
#程序主运行函数
def run():
    ztsj = random.randint(0,300)
    print('暂停{}秒继续执行'.format(ztsj))
    #time.sleep(ztsj)
    postid = getpost()	
    yxsj = qsj()
    ljqdts = zsj(yxsj)
    data = {'msg':'旅行者: ' + yxsj['nickname'] + '\n' + '服务器: ' + yxsj['region_name']+'\n'+'uid:'+ yxsj['nickname'] +'\n' + getjlxx(ljqdts) +'\n'+'本月签到: ' +str(ljqdts)+'次'+'\n'+ yxqd(yxsj) +'\n'+ bbs_sign() +'\n' +"米游社帖子点赞： " + mysdz(postid)+ wxqd() +'\n'}
    return data

# -------  推送模块  --------#
#qmsg推送
def qmsg():
	zz = requests.post(url=qmsg_url.format(qmsg_key),data=run()).json()
	if zz['code'] == 0:
		print(zz['reason'])
		return zz
	else:
		print(zz['reason'])
		return zz
