from main import run,PuSh

# -------  腾讯云函数启动模块  --------#
def main_handler(event,context):
    PuSh()


# -------  本地调试启动模块  --------#
if __name__ == '__main__':
    #print(run())
    PuSh()