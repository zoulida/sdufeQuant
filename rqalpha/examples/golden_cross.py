from rqalpha.api import *

import talib


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    """
           [str] 股票：证券代码，证券的独特的标识符。应以’.XSHG’或’.XSHE’结尾，前者代表上证，后者代表深证。
           期货：期货代码，期货的独特的标识符（郑商所期货合约数字部分进行了补齐。例如原有代码’ZC609’补齐之后变为’ZC1609’）。
           主力连续合约UnderlyingSymbol+88，例如’IF88’ ；指数连续合约命名规则为UnderlyingSymbol+99
           """

    context.s1 = "600016.XSHG"#"000001.XSHE"

    # 设置这个策略当中会用到的参数，在策略中可以随时调用，这个策略使用长短均线，我们在这里设定长线和短线的区间，在调试寻找最佳区间的时候只需要在这里进行数值改动
    context.SHORTPERIOD = 2
    context.LONGPERIOD = 10


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    logger.info("每一个Bar执行")
    logger.info("打印Bar数据：")
    logger.info(bar_dict[context.s1])

    # 开始编写你的主要的算法逻辑
    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # TODO: 开始编写你的算法吧！

    # 因为策略需要用到均线，所以需要读取历史数据
    prices = history_bars(context.s1, context.LONGPERIOD+1, '1d', 'close')

    # 使用talib计算长短两根均线，均线以array的格式表达
    short_avg = talib.SMA(prices, context.SHORTPERIOD)
    long_avg = talib.SMA(prices, context.LONGPERIOD)

    print("short_avg[-1], long_avg[-1]", short_avg[-1], long_avg[-1])
    plot("short avg", short_avg[-1])
    plot("long avg", long_avg[-1])

    #print(context.portfolio.positions)
    # 计算现在portfolio中股票的仓位
    cur_position = context.portfolio.positions[context.s1].quantity
    # 计算现在portfolio中的现金可以购买多少股票
    shares = context.portfolio.cash / bar_dict[context.s1].close

    # 如果短均线从上往下跌破长均线，也就是在目前的bar短线平均值低于长线平均值，而上一个bar的短线平均值高于长线平均值
    if short_avg[-1] - long_avg[-1] < 0 and short_avg[-2] - long_avg[-2] > 0 and cur_position > 0:
        # 进行清仓
        logger.info("进行清仓")
        order_target_value(context.s1, 0)

    # 如果短均线从下往上突破长均线，为入场信号
    if short_avg[-1] - long_avg[-1] > 0 and short_avg[-2] - long_avg[-2] < 0:
        # 满仓入股
        logger.info("满仓入股")
        order_shares(context.s1, shares)
