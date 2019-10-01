__author__ = 'zoulida'
#import tushare as ts
from rqalpha.environment import Environment
from rqalpha.utils.py2 import lru_cache
import pandas as pd
import datetime
import shelve
from rqalpha.const import FILEPATH
import rqalpha.DBStock.mysqlResult as mysqlRS

def singleton(cls):
    instances = {}
    def getinstance(*args,**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return getinstance

@singleton
class MyClass:
    a = 1



'''在上面，我们定义了一个装饰器 singleton，它返回了一个内部函数 getinstance，
该函数会判断某个类是否在字典 instances 中，如果不存在，则会将 cls 作为 key，cls(*args, **kw) 作为 value 存到 instances 中，
否则，直接返回 instances[cls]。'''

@singleton
class MysqlCache():

    def getLastTickPriceByEnvironment(self, rqcode):
        calendar_dt = Environment._env.calendar_dt
        date = calendar_dt.strftime("%Y-%m-%d")
        str_tick = calendar_dt.strftime("%H:%M:%S")
        import rqalpha.utilzld.zhengzeString as zz
        code = zz.getCode(rqcode)
        return self.getLastTickPrice(code, date, str_tick)

    def getLastTickPriceByDateTime(self, rqcode, calendar_dt):
        date = calendar_dt.strftime("%Y-%m-%d")
        str_tick = calendar_dt.strftime("%H:%M:%S")
        import rqalpha.utilzld.zhengzeString as zz
        code = zz.getCode(rqcode)
        return self.getLastTickPrice(code, date, str_tick)

    @lru_cache(1024 * 1024)
    def getLastTickPrice(self, code, date, str_tick):
        if str_tick == '08:55:00ddd' or date == 'mysqltickcache.py  2019-06-11':#debug断点用
            print(date)
            pass#pass不能设断点
        str_tick_value = str_tick
        ticktime = datetime.datetime.strptime(str_tick_value, "%H:%M:%S")
        '''first_tick = datetime.datetime.strptime('9:30:00', "%H:%M:%S")
        if ticktime == first_tick:
            price = self.getTickPrice(code, date, str_tick_value)
            count = 20
            while price is None:
                if count == 0:  # 控制循环次数
                    return None
                count = count - 1
                ticktime = ticktime + datetime.timedelta(seconds=1)  # 时间增加一秒,zoulida
                str_tick_value = ticktime.strftime("%H:%M:%S")
                price = self.getTickPrice(code, date, str_tick_value)
            return price'''


        start_tick = datetime.datetime.strptime('9:29:59', "%H:%M:%S")
        end_tick = datetime.datetime.strptime('15:00:10', "%H:%M:%S")
        close_tick1 = datetime.datetime.strptime('15:00:06', "%H:%M:%S")
        close_tick2 = datetime.datetime.strptime('9:25:30', "%H:%M:%S")

        if  ticktime >= end_tick:  #找到最后一个tick
            ticktime = close_tick1
            str_tick_value = ticktime.strftime("%H:%M:%S")
        if ticktime <= start_tick: #找到第一个tick
            ticktime = close_tick2
            str_tick_value = ticktime.strftime("%H:%M:%S")


        tail_start_tick = datetime.datetime.strptime('14:57:00', "%H:%M:%S")
        tail_end_tick = datetime.datetime.strptime('15:00:00', "%H:%M:%S")
        tail_close_tick = datetime.datetime.strptime('14:57:00', "%H:%M:%S")

        if ticktime >= tail_start_tick and ticktime <= tail_end_tick:  #
            ticktime = tail_close_tick
            str_tick_value = ticktime.strftime("%H:%M:%S")
        saveticktime = ticktime
        price = self.getTickPrice(code, date, str_tick_value)

        count = 30
        while price is None:
            if count == 0: #控制循环次数
                break
            count = count - 1
            ticktime = ticktime - datetime.timedelta(seconds=1)#时间倒退一秒,zoulida
            str_tick_value = ticktime.strftime("%H:%M:%S")
            price = self.getTickPrice(code, date, str_tick_value)

        count = 30
        while price is None:
            if count == 0:  # 控制循环次数
                return None
            count = count - 1
            saveticktime = saveticktime + datetime.timedelta(seconds=1)  # 时间增加一秒,zoulida
            str_tick_value = saveticktime.strftime("%H:%M:%S")
            price = self.getTickPrice(code, date, str_tick_value)

            #print(str_tick)
        return price

    def getTickPrice(self, code, date, tick):
        records = self.getCacheData(code, date)
        #print(records['tick_time'] )
        recordone = records[records['tick_time'] == tick ]
        if recordone.empty :
            return None
        #print(recordone.iloc[0,5])
        return recordone.iloc[0,5]
        pass

    @lru_cache(maxsize = 16 * 1024 * 1024)
    def getdatafromMysql(self, code, date):#获取某一天的tick数据，并缓存在内存

        df = self.getdatafromshelve(code, date)
        '''import rqalpha.DBStock.dbQueryPools as dbpool
        #df = None
        df = dbpool.queryMySQL_tick_stock_market(code, date)
        #print(df)
        #df['date'] = pd.to_datetime(df['date'])
        #df.set_index('Date', inplace=True)
        #reslut = df[(True ^ df['close'].isin([0]))]  # 条件删除去除值为0的行'''

        return df

    def getdatafromshelve(self, code, date):
        #import shelve
        name = code + '_' + str(date)
        dirstr = FILEPATH.SHELVEDIR.value
        file = dirstr + 'TickData'
        print(file, ' ', name)
        try:
            shelveDict = shelve.open(file)
        except Exception as e:
            print('出错，没有文件/volume/shelve/TickData。现在立即新建，并重复执行')
            import os
            os.makedirs('shelve')
            shelveDict = shelve.open(file)

        if name in shelveDict:
            listResult = shelveDict[name]
        else:
            # listResult = haveBeenGreaterThanbyOneDayCodelist(dateDay, percentage)
            import rqalpha.DBStock.dbQueryPools as dbpool
            listResult = dbpool.queryMySQL_tick_stock_market(code, date)
            shelveDict[name] = listResult
        shelveDict.close()
        return listResult

    def getCacheData(self, code, date):
        '''enviroment = Environment.get_instance()
        startdata = enviroment.config.base.start_date
        import datetime
        startdata -= datetime.timedelta(days=365)#获取之前一年的数据，以备函数调用
        enddata = enviroment.config.base.end_date
        #print(startdata)'''
        data = self.getdatafromMysql(code, date)
        #print(data)
        #startstr = start.strftime('%Y-%m-%d')
        #endstr = end.strftime('%Y-%m-%d')
        #result = data.loc[start:end,]
        #result = data.loc[(data['date'] >= start) & (data['date'] <= end) ]
        #print(result)
        return data

    def getHotStockTickByShelve(self, tick):
        filename = 'HotStockTick'
        from rqalpha.const import FILEPATH
        dirstr = FILEPATH.SHELVEDIR.value

        pathname = dirstr + filename
        try:
            shelveDict = shelve.open(pathname)
        except Exception as e:
            print('出错，没有文件%s。现在立即新建，并重复执行' % pathname)
            import os
            os.makedirs(pathname)
            shelveDict = shelve.open(pathname)

        DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        tickstr = tick.strftime(DATETIME_FORMAT)

        if tickstr in shelveDict:
            listResult = shelveDict[tickstr]
        else:
            listResult = self.getHotStockTick(tick)
            shelveDict[tickstr] = listResult
        shelveDict.close()
        return listResult

    def getHotStockTick(self, tick):

        DATETIME_FORMAT = '%Y-%m-%d'
        date = tick.strftime(DATETIME_FORMAT)  # 获得日期
        DATETIME_FORMAT2 = '%H:%M:%S'
        ticktime = tick.strftime(DATETIME_FORMAT2)

        import MysqlTick.Loopback.scanZToneDay3 as scanzt
        # date 日涨停的股票
        listResult = scanzt.getGreaterThanList(date)
        # listResult = getGreaterThanList(dateDay , percentage)
        #print(listResult)
        hotStockList = listResult

        dictHotStock = {}
        for code in hotStockList:  #
            # context.tickbase('600016', '2019-07-25')
            price = self.getTickPrice(code, date, ticktime)
            if price is not None:
                dictHotStock[code] = price
        return dictHotStock

    def getZhangtingStockListbytick(self, tick):
        dictHotStock = self.getHotStockTickByShelve(tick)
        DATETIME_FORMAT = '%Y-%m-%d'
        date = tick.strftime(DATETIME_FORMAT)  # 获得日期
        listZhangting = []
        for code, price in dictHotStock.items():  #
            todayData = mysqlRS.getDayMysqlResult(code, False, date, date)
            import rqalpha.utilzld.zhangtingCalculation as ztprice
            limitUpprice = ztprice.limitUp(todayData['lclose'].iloc[0])

            print(code, price, limitUpprice)
            if price == limitUpprice:
                listZhangting.append(code)
        return listZhangting

    def getZhangtingStockListbytick_Shelve(self, tick):
        filename = 'ZhongtingStockTick'
        from rqalpha.const import FILEPATH
        dirstr = FILEPATH.SHELVEDIR.value

        pathname = dirstr + filename
        try:
            shelveDict = shelve.open(pathname)
        except Exception as e:
            print('出错，没有文件%s。现在立即新建，并重复执行' % pathname)
            import os
            os.makedirs(pathname)
            shelveDict = shelve.open(pathname)

        DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        tickstr = tick.strftime(DATETIME_FORMAT)

        if tickstr in shelveDict:
            listResult = shelveDict[tickstr]
            print(pathname, ' ', tickstr)
        else:
            listResult = self.getZhangtingStockListbytick(tick)
            shelveDict[tickstr] = listResult
        shelveDict.close()
        return listResult

if __name__ =='__main__':

    # c1 = MyClass()
    # c2 = MyClass()
    # print(c1 == c2) # True
    tc = MysqlCache()
    tickstr = '2019-06-03 09:30:07'
    tick = datetime.datetime.strptime(tickstr, "%Y-%m-%d %H:%M:%S")
    ps = tc.getHotStockTickByShelve(tick)
    print(ps)

    #tc.getZhangtingStockListbytick(tick)

    #price = tc.getLastTickPrice('600016', '2019-06-06', '15:00:00')
    #print(price)
    '''tc.getCacheData('000300', True, start ='2018-03-13', end = '2018-05-13')
    tc.getdatafromMysql('000300', True, start ='2018-03-13', end ='2018-05-13')

    tc.getdatafromMysql('000001', False, start='2018-03-13', end='2018-05-13')

    tc.getdatafromMysql('000001', False, start='2018-03-13', end='2018-05-13')

    tc.getdatafromMysql('000001', False, start='2018-03-13', end='2018-05-13')

    tb = MysqlCache().getdatafromMysql('000300', True, start='2018-03-13', end='2018-05-13')
    print(tb)'''

    #pd = tc.getCacheData('600016', '2019-05-13')
    #print(pd)

    #price = tc.getTickPrice('600016', '2019-05-13', '09:25:05')
    #print(price)

'''if __name__ == '__main__':
    ticktime = datetime.datetime.strptime('15:00:00', "%H:%M:%S")
    print(ticktime)
    #mtc = MysqlCache()
    #mtc.getLastTickPrice('600016', '2019-06-06', '15:00:00')'''