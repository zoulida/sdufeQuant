__author__ = 'zoulida'
__author__ = 'zoulida'
#import rqalpha.utilzld.secondsList as secondsList
import datetime
from rqalpha.utilzld.LinkList.LinkedListofTick import tickEliminateOrderedList as tickEliminateOrderedList


def singleton(cls):
    instances = {}
    def getinstance(*args,**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return getinstance

@singleton
class productTicks(): #每天一个MergeTicks
    daysofMachine= {}
    def getNextTick(self, trading_date_str):
        if self.daysofMachine.get(trading_date_str) is not None:
            return self.daysofMachine.get(trading_date_str).getNextTick()
        else:
            self.daysofMachine[trading_date_str] = MergeTicks(trading_date_str)
            return self.daysofMachine[trading_date_str].getNextTick()

    def addBreak(self, trading_date_str, startTickStr, endTickStr):
        self.daysofMachine[trading_date_str].addBreak(startTickStr, endTickStr)

class MergeTicks():
    daysofTick = {}
    beginTime = "09:25:00"  # 写到config
    endTime = "15:00:30"


    breakBeginTime = "11:30:05" #  中午休息
    breakEndTime = "13:00:00"

    def __init__(self, trading_date_str):
        self.trading_date_str = trading_date_str

        self.nextTick = self.beginTime

        self.teol = tickEliminateOrderedList() #采用有序链接表存储tick间断情况，若为1，则后续tick都要输出执行；若为0，则表示删除后续tick，直到遇到1时，再次输出后续tick。
        self.teol.add(self.beginTime, 1)
        self.teol.add(self.endTime, 0)
        self.teol.add(self.breakBeginTime, 0)
        self.teol.add(self.breakEndTime, 1)
        self.stopTick = self.teol.getNextDeactiovTick()


    def getNextTick(self):
        if self.nextTick == None or self.stopTick == None:
            return None
        if self.nextTick <= self.stopTick:
            tickstr = self.trading_date_str + " " + self.nextTick
            tick = datetime.datetime.strptime(tickstr, "%Y-%m-%d %H:%M:%S")
            nextTickFormat = tick + datetime.timedelta(seconds=1)
            self.nextTick = nextTickFormat.strftime("%H:%M:%S")
            return tick
        else:
            self.nextTick = self.teol.getNextActiveTick()
            self.stopTick = self.teol.getNextDeactiovTick()
            if self.stopTick == None:
                return None
            else:
                return self.getNextTick()

    def addBreak(self, startTickStr, endTickStr):#输入中断信息。查询时，只需找到下一个key为1的tick就行，不管后续有几个0.
        beginDateSecond = datetime.datetime.strptime(startTickStr, "%H:%M:%S")
        #endDateSecond = datetime.datetime.strptime(endTickStr, "%H:%M:%S")
        beginDateSecond = beginDateSecond + datetime.timedelta(seconds=2)  # zoulida 增加一秒处理订单

        beginDateSecondStr = beginDateSecond.strftime("%H:%M:%S")
        if self.stopTick > beginDateSecondStr:
            self.stopTick = beginDateSecond.strftime("%H:%M:%S")

        #self.teol.add(startTickStr, 0)
        #self.teol.add(endTickStr, 1)
        self.teol.addBreak(startTickStr, endTickStr)


if __name__ == '__main__':
    pt = productTicks()
    tick = pt.getNextTick('2019-08-08')
    print(tick)

    tick = pt.getNextTick('2019-08-08')
    print(tick)

    pt.addBreak('2019-08-08', '10:30:05', '14:30:05')

    while tick is not None:
        print(tick)
        tick = pt.getNextTick('2019-08-08')

        debugtick =  datetime.datetime.strptime('2019-08-08 11:30:05', "%Y-%m-%d %H:%M:%S")
        if tick == debugtick:
            print(' tttttttttttttttttt ', tick)
