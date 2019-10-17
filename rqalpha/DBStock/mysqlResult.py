__author__ = 'zoulida'
from rqalpha.utils.py2 import lru_cache

@lru_cache( maxsize = None)
def getDayMysqlResult(code, indexboolean, start, end):
    # return ts.get_k_data(code, index=index, start=start, end=end)
    from .mysqlCache import MysqlCache
    tc = MysqlCache()
    result = tc.getCacheData(code, indexboolean, start, end)
    return result

if __name__ == '__main__':
    tddata = getDayMysqlResult('600016', False, '2019-06-03', '2019-06-03')
    print(tddata)
    pass