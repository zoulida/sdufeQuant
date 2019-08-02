__author__ = 'zoulida'
import rqalpha.utilzld.secondsList as secondsList

def singleton(cls):
    instances = {}
    def getinstance(*args,**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return getinstance

@singleton
class ELiminateTicks():
    seconds = []
    def getELTicks(self):
        return self.seconds
    def cleanTicks(self):
        self.seconds = []
    def addTicks(self, seconds):
        self.seconds.append(seconds)
        pass
    def removeTicks(self):
        pass
    def addTicks(self, beginDateSecond, endDateSecond):
        seconds = secondsList.dateSecondRangeByDatatime(beginDateSecond, endDateSecond)
        self.addTicks(seconds)
    def addTicksbyString(self, beginDateSecondstr, endDateSecondstr):

        pass