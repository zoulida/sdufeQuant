__author__ = 'zoulida'

from memory_profiler import profile

@profile
def my_func():
    print('dddd')
    list = ['1'  , 'dd']
    print(list)
    count = 1000000
    while count != 0:
        list.append('fffffffffffffffffffffffffffffffffffff')
        count = count - 1

    print("end")

@profile
def test():
    my_func()
    print('test')

if __name__ == '__main__':
    #my_func()
    test()