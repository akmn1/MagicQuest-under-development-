import os
from core import cursor
# 设置项目根目录为全局变量
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if __name__ == "__main__":
    cursor.apply_cursor()
