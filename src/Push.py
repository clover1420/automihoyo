import requests
from src.logger import Log
logger = Log()

class Push():
    """
    msg : 消息内容
    push ： 推送的配置
    """
    def __init__(self,msg,push) -> None:
        self.qmsg_key = push['PushKey']['Qmsg']
        self.Server_key = push['PushKey']['Server']
        self.msg = msg
        pass

    #qmsg酱推送
    def Qmsg(self) -> None:
        if self.qmsg_key == "":
            logger.info("没有配置qmsg酱key")
        else:
            try:
                qmsg_url = f'https://qmsg.zendee.cn/send/{self.qmsg_key}'
                data = {'msg': "米游社原神签到\n"+self.msg}
                zz = requests.post(url=qmsg_url,data=data).json()
                if zz['code'] == 0:
                    logger.info("qmsg酱"+zz['reason'])
                else:
                    logger.info("qmsg酱"+zz['reason'])
            except Exception as e:
                logger.error("qmsg酱可能挂了:"+e)

    #Sever酱推送
    def Server(self,title="米游社签到") -> None:
        if self.Server_key == "":
            logger.info("没有Server酱cookie")
        else:
            Server_url = f"https://sctapi.ftqq.com/{self.Server_key}.send"
            data = {
                "title":title,
                "desp":self.msg
            }
            zz = requests.post(url=Server_url,data=data).json()
            if zz['code'] == "0":
                logger.info("Server推送成功")
            else:
                logger.info("Server推送失败"+zz['message'])

