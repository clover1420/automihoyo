import requests,time
from Functional import Mys_bbs
from Functional import YsReward
from config import *

# -------  运行模块  --------#
#程序主运行函数
def run():
	if mihoyo_bbs == "":
		print("没有米游社论坛cookie")
		bbsdata = "没有米游社论坛cookie\n"
	else:
		bbs = Mys_bbs(mihoyo_bbs)
		post_id = bbs.GetPostId('26')
		for k in range(0,10):
				dzfh = bbs.ThumbsUp(post_id[k])
				time.sleep(0.4)
		for i in gameList:
			qd = bbs.bbs_sign(i['id'])
		for j in range(0,3):
			kt = bbs.Latsk(post_id[j])
		fx = bbs.Share(post_id[0])
		bbsdata = '论坛签到'+ qd +'\n' +"米游社帖子点赞： " + dzfh + '\n'
	if YsRewardCookie == "":
		print("没有原神签到cookie")
		ysdata = "没有原神签到cookie\n"
	else:
		ys = YsReward(YsRewardCookie)
		uid = ys.GetGameUid()
		day = ys.GetCumulativeSign(uid)
		reward = ys.Getjlxx(day)
		sign = ys.Sign(uid)
		ysdata = '旅行者: ' + uid['nickname'] + '\n' + '服务器: ' + uid['region_name']+'\n'+'uid:'+ uid['nickname'] +'\n' + sign +'\n'+'本月签到: ' +str(day)+'次\n'+ reward +'\n'
	data = {'msg':ysdata + bbsdata}
	return data

# -------  推送模块  --------#
#qmsg推送
def qmsg():
	try:
		qmsg_url = 'https://qmsg.zendee.cn/send/{}'
		zz = requests.post(url=qmsg_url.format(qmsg_key),data=run()).json()
		if zz['code'] == 0:
			print(zz['reason'])
			return zz
		else:
			print(zz['reason'])
			return zz
	except Exception:
		print("qmsg酱可能挂了")