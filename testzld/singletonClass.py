__author__ = 'zoulida'


class people(object):
    def __new__(cls, *args, **kargs):
        return super(people, cls).__new__(cls)

    def __init__(self, name):
        self.name = name

    def talk(self):
        print("hello,I am %s" % self.name)


class student(people):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(student, cls).__new__(cls, *args, **kargs)
        return cls.instance

    def __init__(self, name):
        if not hasattr(self, "init_fir"):
            self.init_fir = True
            super(student, self).__init__(name)


a = student("Timo")
print(a)
b = student("kysa")
c = student("Luyi")
a.talk()
b.talk()
print(c)
