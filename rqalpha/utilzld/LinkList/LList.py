__author__ = 'zoulida'
class Node:
    def __init__(self, init_data):
        self.data = init_data
        self.next = None

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next

    def set_data(self, new_data):
        self.data = new_data

    def set_next(self, new_next):
        self.next = new_next


class orderedList:#有序
    def __init__(self):
        self.head = None

    def __str__(self):
        print_list = []
        current = self.head
        while current is not None:
            print_list.append(current.get_data())
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

    def add(self, item):
        current = self.head
        previous = None
        while current is not None:
            if current.get_data() > item:
                break
            previous = current
            current = current.get_next()
        temp = Node(item)
        if previous is None:
            temp.set_next(self.head)
            self.head = temp
        else:
            temp.set_next(current)
            previous.set_next(temp)

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
            if current.get_data() == item:
                return True
            if current.get_data() > item:
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
            while self.index(current.get_data()) != pos:
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
        while self.index(current.get_data()) != index:
            previous = current
            current = current.get_next()
        item = current.get_data()
        if previous is None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())
        return item


class UnorderedList:#无序
    def __init__(self):
        self.head = None

    def __str__(self):
        print_list = []
        current = self.head
        while current is not None:
            print_list.append(current.get_data())
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

    def add(self, item): #在头部插入
        temp = Node(item)
        temp.set_next(self.head)
        self.head = temp

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
            if current.get_data() == item:
                return True
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
            while self.index(current.get_data()) != pos:
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
        while self.index(current.get_data()) != index:
            previous = current
            current = current.get_next()
        item = current.get_data()
        if previous is None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())
        return item

if __name__ == '__main__':
    orderlist = orderedList()
    orderlist.add(9)
    orderlist.add(5)
    orderlist.add(10)
    orderlist.add(3)
    orderlist.add(1)
    print(orderlist)