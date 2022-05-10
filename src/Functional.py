import requests
import hashlib
import time
import random
import string
from src.logger import Log
logger = Log()

# -------  加密算法类 --------#
class Encryption():
    #生成MD5
    def md5(self,text):
        md5 = hashlib.md5()
        md5.update(text.encode())
        return md5.hexdigest()

    #生成指定位数随机字符串
    def randomStr(self,n):
        return (''.join(random.sample(string.ascii_lowercase, n))).upper()

    #ys-web-ds算法函数 
    def get_web_DS(self):
        n = "h8w582wxwgqvahcdkpvdhbh2w9casgfl"  #2.3.0
        #n = 'cx2y9z9a29tfqvr1qsq6c7yz99b5jsqt'  2.2.1
        i = str(int(time.time()))
        r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
        c = self.md5("salt=" + n + "&t=" + i + "&r=" + r)
        return "{},{},{}".format(i, r, c)

    #bbs-ds算法函数 
    def get_bbs_DS(self):
        #n = "h8w582wxwgqvahcdkpvdhbh2w9casgfl"
        #n = "14bmu1mz0yuljprsfgpvjh3ju2ni468r"
        n = "fd3ykrh7o1j54g581upo1tvpam0dsgtf" #2.7.0
        i = str(int(time.time()))
        r = self.randomStr(6)
        c = self.md5("salt=" + n + "&t=" + i + "&r=" + r)
        return "{},{},{}".format(i, r, c)

# -------  米游社论坛类  --------#
class Mys_bbs():
    share_url = "https://bbs-api.mihoyo.com/apihub/api/getShareConf?entity_id={}&entity_type=1"
    plate_signin_url = "https://bbs-api.mihoyo.com/apihub/sapi/signIn?gids={}"
    post_url = "https://bbs-api.mihoyo.com/post/api/getForumPostList?forum_id={}&is_good=false&is_hot=false&page_size=20&sort_type=1"
    see_post_url = 'https://bbs-api.mihoyo.com/post/api/getPostFull?post_id={}'
    Like_url = 'https://bbs-api.mihoyo.com/apihub/sapi/upvotePost'
    def __init__(self,bbs_cookie) -> None:
        ds = Encryption()
        self.headers = {
			'DS':ds.get_bbs_DS(),
			'cookie':bbs_cookie,
			'x-rpc-client_type':'2',
			'x-rpc-app_version':'2.7.0',
			'x-rpc-sys_version':'12',
			'x-rpc-device_id':'818b3153-e80a-3697-81db-f96cc9c693de',
			'x-rpc-channel':'xiaomi',
			'x-rpc-device_name':'Xiaomi M2012K11AC',
			'x-rpc-device_model':'M2012K11AC',
			'host':'bbs-api.mihoyo.com',
			'referer':'https://app.mihoyo.com'
		}

    #论坛签到函数
    def bbs_sign(self,bbsid):
        zz = requests.post(url=self.plate_signin_url.format(bbsid),headers=self.headers).json()
        if zz['message'] == 'OK':
            logger.info("签到成功")
            return "签到成功"
        else:
            logger.info(zz['message'])
            return zz['message']

	#获取帖子id
    def GetPostId(self,bbsid):
        post_id = []
        dzysj = requests.get(url=self.post_url.format(bbsid)).json()
        for x in dzysj['data']['list']:
            post_id.append(x['post']['post_id'])
        return post_id

    #分享贴子
    def Share(self,post_id):
        zz = requests.get(url=self.share_url.format(post_id),headers=self.headers).json()
        if zz['message'] == 'OK':
            logger.info('分享帖子：成功')
            return "分享帖子：成功"
        else:
            logger.info('分享帖子：失败')
            return "分享帖子：失败"

    #看贴
    def Latsk(self,post_id):
        zz = requests.get(self.see_post_url.format(post_id),headers=self.headers).json()
        if zz['message'] == 'OK':
            logger.info('看贴成功')
        else:
            logger.info('看贴失败'+zz['message'])
        return "看贴："+ zz['message']

    #米游社帖子点赞
    def ThumbsUp(self,post_id):
        data = '{"is_cancel":false,"post_id":"'+ post_id +'"}'
        dafh = requests.post(url=self.Like_url,data=data,headers=self.headers).json()
        if dafh['message'] == 'OK':
            logger.info('点赞帖子：成功')
            return "成功"
        else:
            logger.info('点赞帖子：失败')
            return "失败"

# -------  原神游戏每日签到类  --------#
class YsReward():
    """
    YsCookie : 原神签到cookie
    """
    Todays_reward_url = "https://api-takumi.mihoyo.com/event/bbs_sign_reward/home?act_id=e202009291139501"
    get_Game_uid = "https://api-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz=hk4e_cn"
    get_Cumulative_check_in_url = "https://api-takumi.mihoyo.com/event/bbs_sign_reward/info?region={}&act_id={}&uid={}"
    Check_in_daily_url = "https://api-takumi.mihoyo.com/event/bbs_sign_reward/sign"
    def __init__(self,YsCookie) -> None:
        ds = Encryption()
        self.heades = {
            'User-Agent':'Mozilla/5.0 (Linux; Android 7.0; Meizu S6 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.110 Mobile Safari/537.36 miHoYoBBS/2.2.0',
            'x-rpc-device_id':'2eee2fdb-0cc1-3f25-8e5c-0e2b06439cbd',
            'referer':'https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required=true&act_id=e202009291139501&utm_source=bbs&utm_medium=mys&utm_campaign=icon',
            'x-rpc-app_version':'2.3.0',
            'Host':'api-takumi.mihoyo.com',
            'x-rpc-client_type':'5',
            'Content-Type':'application/json;charset=UTF-8',
            'Accept':'application/json, text/plain, */*',
            'cookie':YsCookie,
            'X-Requested-With':'com.mihoyo.hyperion',
            'ds':ds.get_web_DS()
        }
    
    #获取游戏uid函数
    def GetGameUid(self):
        zz = requests.get(url=self.get_Game_uid,headers=self.heades).json()
        return zz['data']['list'][0]

    #获取累计签到函数
    def GetCumulativeSign(self,uid):
        """
        uid : 获取游戏uid方法的返回值
        """
        url = self.get_Cumulative_check_in_url.format(uid['region'],'e202009291139501',uid['game_uid'])
        zz = requests.get(url=url,headers=self.heades).json()
        return zz['data']['total_sign_day']

    #获取今日奖励信息函数
    def Getjlxx(self,day):
        zz = requests.get(url=self.Todays_reward_url,headers=self.heades).json()
        sy = int(day)
        logger.info('今日奖励: ' + zz["data"]['awards'][sy]['name'] + ' x ' + str(zz["data"]['awards'][sy]['cnt']))
        return '今日奖励: ' + zz["data"]['awards'][sy]['name'] + ' x ' + str(zz["data"]['awards'][sy]['cnt'])
    
    #游戏每日签到函数
    def Sign(self,uid):
        """
        uid : 获取游戏uid方法的返回值
        """
        data = '{"act_id":"e202009291139501","region":"'+ uid['region'] +'","uid":"'+ uid['game_uid'] +'"}'
        zz = requests.post(url=self.Check_in_daily_url,data=data,headers=self.heades).json()
        if zz['message'] == 'OK':
            fh = '签到结果: 签到完成'
        else:	
            fh = '签到结果: ' + zz['message']
        logger.info(fh)
        return fh