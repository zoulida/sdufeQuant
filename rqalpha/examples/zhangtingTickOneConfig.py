__author__ = 'zoulida'
from rqalpha import run
from guppy import hpy

def init():

    import os
    import sys
    #strategy_file_path = context.config.base.strategy_file
    print(sys.path)
    print('/volume/pythonworkspace/rqalpha/rqalpha/examples')
    sys.path.append('/volume/pythonworkspace/rqalpha/rqalpha/examples')

config = {
    "base": {
        "strategy_file": "zhangtingTickOneStrategy.py",#"examples/buy_and_hold_Tick.py"""./examples/buy_and_hold.py",examples/golden_cross.py
        "start_date": "2019-04-11",
        "end_date": "2019-04-12",
        "frequency": "tick",
        "accounts": {
            "stock": 100000
        },
        "benchmark":"000001.XSHG"

    },
    "mod": {
        "mysql": {
                     "enabled": True
                 },
        "tushare": {
                     "enabled": False
                 },
        "sys_analyser": {
            "enabled": True,
            "plot": True,
            # 当不输出csv/pickle/plot 等内容时，可以通过 record 来决定是否执行该 Mod 的计算逻辑
            "record": True,
            # 如果指定路径，则输出计算后的 pickle 文件
            "output_file": "result.pkl",
            # 如果指定路径，则输出 report csv 文件
            "report_save_path": ".",
            # 画图
            'plot': True,
            # 如果指定路径，则输出 plot 对应的图片文件
            'plot_save_file': "result.png"
        },
        "sys_simulation": {
           "matching_type": "tick_current_bar"
            # "matching_type": "current_bar"
        }

    }
}
#init()

from memory_profiler import profile
@profile
def startRun():
    run(config)


if __name__ == '__main__':
    startRun()
#mem = hpy()
#print(mem.heap())