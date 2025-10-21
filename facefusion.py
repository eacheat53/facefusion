#!/usr/bin/env python3
import os
import pyfiglet

# 清屏（可选）
os.system('cls' if os.name == 'nt' else 'clear')

# 标题大字
big_text = pyfiglet.figlet_format("FaceFusion", font="slant")

# 构建极简展示块
banner = f"""
{big_text.rstrip()}
"""

print(banner)

# 如果您想保留启动时的分割线，可以取消下面这行的注释
# print("\n" + "═" * 80 + "\n")

# 如果您想保留启动时的5秒等待，可以取消下面这行的注释
# import time
# time.sleep(5)

# 核心环境变量设置
os.environ['OMP_NUM_THREADS'] = '1'

# 导入并运行主程序
from facefusion import core

if __name__ == '__main__':
    core.cli()
