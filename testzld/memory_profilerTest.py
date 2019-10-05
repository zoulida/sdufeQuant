__author__ = 'zoulida'

from memory_profiler import profile

@profile
def my_func():
    print('dddd')

if __name__ == '__main__':
    my_func()