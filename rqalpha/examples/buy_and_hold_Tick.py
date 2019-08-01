from rqalpha.api import *
import time
import MysqlTick.Loopback.mysqlTickCache as tickCache

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    logger.info("init")
    context.s1 = "600519.XSHG"
    context.cc = "600016.XSHG"
    update_universe(context.s1)
    # 是否已发送了order
    context.fired = False
    context.tickbase = tickCache.MysqlCache()

def before_trading(context):
    logger.info('before_trading')
    pass

#1.全仓买入第一个涨停的。2.第2天开盘价卖出
def handle_tick(context, tick):
    logger.info("每一个Tick执行")
    logger.info(tick)

    DATETIME_FORMAT = '%Y-%m-%d'
    date = tick.strftime(DATETIME_FORMAT)  # 获得日期

    DATETIME_FORMAT2 = '%H:%M:%S'
    ticktime = tick.strftime(DATETIME_FORMAT2)
    if ticktime ==  '09:25:00':#每天这个时间要做数据准备工作
        print(ticktime)
        import MysqlTick.Loopback.scanZToneDay3 as scanzt

        listResult = scanzt.getGreaterThanList(date)
        # listResult = getGreaterThanList(dateDay , percentage)
        print(listResult)
        context.hotStockList = listResult

    for code in context.hotStockList:#
        context.tickbase('600016', '2019-07-25')
        pass
        #print(code)



    '''import rqalpha.DBStock.mysqlResult as mysqlRS
    todayData = mysqlRS.getDayMysqlResult('600016', False, date, date)
    #logger.info(todayData)'''
    #time.sleep(1)#调试时方便查看log

    '''from rqalpha.environment import Environment   #Environment有很多信息
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
    dt = Environment.get_instance().calendar_dt.strftime(DATETIME_FORMAT)
    print('ddddddddddddd', dt)'''


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    logger.info("每一个Bar执行")
    logger.info("打印Bar数据：")
    logger.info(bar_dict[context.cc])
    logger.info(bar_dict[context.s1])

    # TODO: 开始编写你的算法吧！
    if not context.fired:
        # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
        order_percent(context.s1, 1)
        context.fired = True
