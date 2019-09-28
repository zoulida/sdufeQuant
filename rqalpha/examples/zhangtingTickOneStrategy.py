from rqalpha.api import *
import time
import datetime
import MysqlTick.Loopback.mysqlTickCache as tickCache
import rqalpha.DBStock.mysqlResult as mysqlRS
from rqalpha.const import DEFAULT_ACCOUNT_TYPE

import rqalpha.utilzld.codeStrChange as codeStrChange
codeChange = codeStrChange.CodeChange()

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    logger.info("init")
    context.s1 = "600519.XSHG"
    context.cc = "600016.XSHG"
    context.todayBuy = {}#逻辑是当天买入的股票，不管是否有以前的仓位，一律不准卖出。
    update_universe(context.s1)
    # 是否已发送了order
    context.fired = False
    context.tickbase = tickCache.MysqlCache()

    global timeBeginStrategy
    timeBeginStrategy = datetime.datetime.now()

def before_trading(context):
    logger.info('before_trading everyday')
    context.todayBuy = {}

    pass

def after_trading(context):
    logger.info('after_trading everyday')
    endTimeStrategy = datetime.datetime.now()
    strategyTime = endTimeStrategy - timeBeginStrategy
    print('strategyTime is ', strategyTime)
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

        #date 日涨停的股票
        listResult = scanzt.getGreaterThanList(date)
        # listResult = getGreaterThanList(dateDay , percentage)
        print(listResult)
        context.hotStockList = listResult


        #去掉 9点25分到9点29分的tick
        import rqalpha.utilzld.eliminateTicks as ET
        el = ET.ELiminateTicks()
        beginTick = date + ' ' + '09:25:00'
        endTick = date + ' ' + '09:29:59'
        el.addTicksbyString(beginTick, endTick)
        elticks = el.getELTicks()
        import rqalpha.utilzld.mergeTicks as MT
        mt = MT.MergeTicks()
        mt.munisTicks(date, elticks)
        #print(mt.getTicksbyStrDay(date))

        return

    #先卖后买
    #print(context.portfolio.positions)
    if context.portfolio.positions.__len__() > 0:
        codeSell = context.portfolio.positions.keys()[0]#这里逻辑是只有一只股票，若是有多只则要遍历
        account = context.portfolio.accounts[DEFAULT_ACCOUNT_TYPE.STOCK.name]
        position = account.positions[codeSell]
        sellable = position.sellable
        if sellable > 0:
            print('检测到持有非冻结股票，立即清盘！！！   ')
            if ticktime >= '09:30:00':
                logger.info("进行清仓")
                order_target_value(codeSell, 0)
                return  # 当前tick不能卖，所以也没有cash买了。返回吧
            else:
                print('只能在9：30：00以后清盘')
                return  # 清仓前，没有资金了，无法购买，直接返回。'''
        '''if codeSell not in context.todayBuy and sellable > 0:
            print('持有股票，立即清盘！！！   ')
            
            priceSell = context.tickbase.getTickPrice(codeChange.getNCode(codeSell), date, ticktime)
            if priceSell is not None:
                logger.info("进行清仓")
                order_target_value(codeSell, 0)
                return #当前tick不能卖，所以也没有cash买了。返回吧
            else:
                print('没有报价，无法清盘') #没有报价，要去数库主动查找。
                return #清仓前，没有资金了，无法购买，直接返回。'''

    for code in context.hotStockList:#
        #context.tickbase('600016', '2019-07-25')
        price = context.tickbase.getTickPrice(code, date, ticktime)
        if price is not None:#并不是每个股票每个tick秒都有数据
            #print(price)
            todayData = mysqlRS.getDayMysqlResult(code, False, date, date)
            #print('tttt',todayData['lclose'].iloc[0])
            import rqalpha.utilzld.zhangtingCalculation as ztprice

            limitUpprice = ztprice.limitUp(todayData['lclose'].iloc[0])
            #print(price, limitUpprice)
            if price == limitUpprice:
                print(todayData)
                print('buybuybuy!!!!!!!!!!!!!!!')

                riceCode = codeChange.getRiceCode(code)
                order_percent(riceCode, 1)
                context.todayBuy[riceCode] = 0


                #time.sleep(3)


                eliminteTicks(date, ticktime) ## 去掉当天 所有后续时间的tick
                #eliminteTicks(date, ticktime)


                return



def eliminteTicks(date, ticktime):
    # 去掉当天 所有后续时间的tick
    import rqalpha.utilzld.eliminateTicks as ET
    el = ET.ELiminateTicks()
    beginTick = date + ' ' + ticktime
    endTick = date + ' ' + '15:00:30'
    el.addTicksbyString(beginTick, endTick)
    import rqalpha.utilzld.mergeTicks as MT
    mt = MT.MergeTicks()
    elticks = el.getELTicks()
    mt.munisTicks(date, elticks)




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
