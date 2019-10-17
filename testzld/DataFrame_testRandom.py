__author__ = 'zoulida'

import pandas as pd
from memory_profiler import profile

@profile
def random():
    min_date = pd.to_datetime('1960-01-01')
    max_date = pd.to_datetime('1990-12-31')

    d = (max_date - min_date).days + 1

    df = pd.DataFrame()
    df['dob'] = min_date + pd.to_timedelta(pd.np.random.randint(d, size=88799), unit='d')

    print(df)

    del df
    import gc
    gc.collect()


@profile
def test():
    print('aaaaaa')
    random()
    print('ffffff')

if __name__ == '__main__':
    test()
