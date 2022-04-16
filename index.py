from main import run,qmsg

# -------  腾讯云函数启动模块  --------#
def main_handler(event,context):
    qmsg()


# -------  本地调试启动模块  --------#
if __name__ == '__main__':
	print(run())