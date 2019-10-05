__author__ = 'zoulida'
'''from memory_profiler import profile
from hashlib import sha1
import sys

@profile
def my_func():
    sha1Obj = sha1()
    with open(sys.argv[1], 'rb') as f:
        while True:
            buf = f.read(10 * 1024 * 1024)
            if buf:
                sha1Obj.update(buf)
            else:
                break

    print(sha1Obj.hexdigest())'''




from guppy import hpy
import sys


def my_func():
    mem = hpy()
    strdd = 'dddd'

    print(mem.heap())


if __name__ == '__main__':
    my_func()