__author__ = 'zoulida' #这个是从mod里复制出来的，注意代码要同步。
import tushare as ts
from rqalpha.environment import Environment
from rqalpha.utils.py2 import lru_cache
import pandas as pd
from rqalpha.const import FILEPATH

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

    @lru_cache(1024 * 1024 * 48)
    def getdatafromMysql(self, code, index, startdate, enddate):
        '''#startstr = start.strftime('%Y-%m-%d')
        #endstr = end.strftime('%Y-%m-%d')
        #reslut = ts.get_k_data(code, index=index, start=startstr, end=endstr)
        import rqalpha.DBStock.dbQueryPools as dbpool
        df = dbpool.queryMySQL_plot_stock_market(code, start, end)
        df['date'] = pd.to_datetime(df['date'])
        #df.set_index('Date', inplace=True)
        reslut = df[(True ^ df['close'].isin([0]))]  # 条件删除去除值为0的行'''

        reslut = self.getdatafromshelve(code, startdate, enddate)


        return reslut

    def getdatafromshelve(self, code, startdate, enddate):
        import shelve
        dirstr = FILEPATH.SHELVEDIR.value
        file = dirstr + 'DayData'

        name = code + '_' + str(startdate) + '_' + str(enddate)
        print(file, ' ', name)
        shelveDict = shelve.open(file)
        if name in shelveDict:
            listResult = shelveDict[name]
        else:
            import rqalpha.DBStock.dbQueryPools as dbpool
            df = dbpool.queryMySQL_plot_stock_market(code, startdate, enddate)
            df['date'] = pd.to_datetime(df['date'])
            # df.set_index('Date', inplace=True)
            listResult = df[(True ^ df['close'].isin([0]))]  # 条件删除去除值为0的行


            shelveDict[name] = listResult
        shelveDict.close()

        return listResult

    def getCacheData(self, code, index, start, end):#index 是boolean。
        enviroment = Environment.get_instance()
        startdata = enviroment.config.base.start_date
        import datetime
        startdata -= datetime.timedelta(days=365)#获取之前一年的数据，以备函数调用
        enddata = enviroment.config.base.end_date
        #print(startdata)
        data = self.getdatafromMysql(code, index, startdata, enddata)

        result = data.loc[(data['date'] >= start) & (data['date'] <= end) ]
        #print(result)
        return result

if __name__ =='__main__':
    # c1 = MyClass()
    # c2 = MyClass()
    # print(c1 == c2) # True
    tc = MysqlCache()
    tc.getCacheData('000300', True, start ='2018-03-13', end = '2018-05-13')
    tc.getdatafromMysql('000300', True, start ='2018-03-13', end ='2018-05-13')

    tc.getdatafromMysql('000001', False, start='2018-03-13', end='2018-05-13')

    tc.getdatafromMysql('000001', False, start='2018-03-13', end='2018-05-13')

    tc.getdatafromMysql('000001', False, start='2018-03-13', end='2018-05-13')

    tb = MysqlCache().getdatafromMysql('000300', True, start='2018-03-13', end='2018-05-13')
    print(tb)