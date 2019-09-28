__author__ = 'zoulida'
#沪市A股票买卖的代码是以600、601或603打头；深市A股票买卖的代码是以000打头，中小板（也属于深市）股票代码以002打头，创业板（也属于深市）股票代码以300打头
"""[str] 股票：证券代码，证券的独特的标识符。应以’.XSHG’或’.XSHE’结尾，前者代表上证，后者代表深证。
        期货：期货代码，期货的独特的标识符（郑商所期货合约数字部分进行了补齐。例如原有代码’ZC609’补齐之后变为’ZC1609’）。
        主力连续合约UnderlyingSymbol+88，例如’IF88’ ；指数连续合约命名规则为UnderlyingSymbol+99
        """

def singleton(cls):
    instances = {}
    def getinstance(*args,**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return getinstance

@singleton
class CodeChange():
    def getRiceCode(self, code):
        if code.startswith('6'):
            return code + '.XSHG'
        else:
            return code + '.XSHE'
    def getNCode(self, RiceCode):
        return RiceCode[:6]


if __name__ == '__main__':
    cc = CodeChange()
    coderq = cc.getRiceCode('000001')
    print(coderq)