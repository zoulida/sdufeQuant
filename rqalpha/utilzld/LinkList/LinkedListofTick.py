__author__ = 'zoulida'
class Node:
    def __init__(self, key, value = 0):
        self.key = key
        self.value = value
        self.next = None

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def get_next(self):
        return self.next

    def set_value(self, new_value):
        self.value = new_value

    def set_next(self, new_next):
        self.next = new_next


class orderedList:#有序
    def __init__(self):
        self.head = None
        self.cursor = None

    def __str__(self):
        print_list = []
        current = self.head
        while current is not None:
            print_list.append(current.get_key())
            print_list.append(current.get_value())
            current = current.get_next()
        return str(print_list)

    def is_empty(self):
        return self.head is None

    def size(self):
        current = self.head
        count = 0
        while current is not None:
            count += 1
            current = current.get_next()
        return count

    def add(self, item, value = 0):
        current = self.head
        previous = None
        while current is not None:
            if current.get_key() > item:
                break
            previous = current
            current = current.get_next()
        temp = Node(item, value )
        if previous is None:
            temp.set_next(self.head)
            self.head = temp
        else:
            temp.set_next(current)
            previous.set_next(temp)
        return temp



    def remove(self, item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.get_data() == item:
                found = True
            else:
                previous = current
                current = current.get_next()
        if previous is None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())

    def search(self, item):
        current = self.head
        while current is not None:
            if current.get_key() == item:
                return True
            if current.get_key() > item:
                return False
            else:
                current = current.get_next()
        return False

    def insert(self, pos, item):
        node = Node(item)
        if pos == 0:
            node.set_next(self.head)
            self.head = node
        else:
            current = self.head
            previous = None
            while self.index(current.get_key()) != pos:
                previous = current
                current = current.get_next()
                if current is None:
                    break
            previous.set_next(node)
            node.set_next(current)

    def pop(self, index=None):
        if index is None:
            index = self.size() - 1
        if index < 0:
            index = self.size() - abs(index)
        if index < 0 or (index >= self.size()):
            raise IndexError
        current = self.head
        previous = None
        while self.index(current.get_key()) != index:
            previous = current
            current = current.get_next()
        item = current.get_key()
        if previous is None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())
        return item

    def index(self, item):
        index = 0
        current = self.head
        while current is not None:
            if current.get_data() == item:
                return index
            current = current.get_next()
            index += 1
        return -1


class tickEliminateOrderedList(orderedList):

    def __init__(self):
        super(tickEliminateOrderedList, self).__init__()
        self.add('00:00:01', 0) #生成一个假头

    def addBreak(self, startTickStr, endTickStr):
        node1 = self.add(startTickStr, 0)
        node2 = self.add(endTickStr, 1)
        if self.cursor.get_key() > node1.get_key():
            self.cursor = node1
            self.connect(node1, node2)

    def connect(self, node1, node2):
        node1.set_next(node2)

    #self.cursor = None
    def getNextActiveTick(self):
        if self.head == None:
            raise Exception("Exception self.head == None")
        if self.cursor == None:
            self.cursor = self.head

        self.cursor = self.cursor.get_next()
        if self.cursor is None:
            return None
        if self.cursor.get_value() == 0:
            return self.getNextActiveTick()
        else:
            return self.cursor.get_key()

    def getNextDeactiovTick(self):
        if self.head == None:
            raise Exception("Exception self.head == None")
        if self.cursor == None:
            self.cursor = self.head

        self.cursor = self.cursor.get_next()
        if self.cursor is None:
            return None
        if self.cursor.get_value() == 1:
            return self.getNextDeactiovTick()
        else:
            return self.cursor.get_key()


if __name__ == '__main__':
    orderlist = tickEliminateOrderedList()
    orderlist.add('9', 1)
    orderlist.add('5', 0)
    orderlist.add('10', 0)
    orderlist.add('3', 1)
    orderlist.add('1', 0)
    print(orderlist)
    tmp = orderlist.getNextDeactiovTick()
    print(tmp)