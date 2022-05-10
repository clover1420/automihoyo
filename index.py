from main import run,PuSh
from src.Push import Push

# -------  腾讯云函数启动模块  --------#
def main_handler(event,context):
    PuSh()


# -------  本地调试启动模块  --------#
if __name__ == '__main__':
    PuSh()