__author__ = 'zoulida'
import objgraph

_cache = []


class OBJ(object):
    pass


def func_to_leak():
    o = OBJ()
    _cache.append(o)
    # do something with o, then remove it from _cache

    if True:  # this seem ugly, but it always exists
        return
    _cache.remove(o)


if __name__ == '__main__':
    try:
        func_to_leak()
    except:
        pass
    objgraph.show_backrefs(objgraph.by_type('OBJ')[0], max_depth=10, filename='obj2.dot')
