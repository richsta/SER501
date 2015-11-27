# -*- coding: utf-8 -*-

"""
Created on Mon Oct 5 18:31:27 2015
@author: Richa
"""


import random
import Queue

class SinglyLinkedNode(object):
    """
    >>> a=SinglyLinkedNode()
    >>> a.__init__()
    """

    def __init__(self, item=None, next_link=None):
        super(SinglyLinkedNode, self).__init__()
        self._item = item
        self._next = next_link

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    def __repr__(self):
        return repr(self.item)


class SinglyLinkedList(object):
    """
    >>> a=SinglyLinkedList()
    >>> a.prepend(4)
    >>> a.prepend(2)
    >>> a.__contains__(4)
    True
    >>> a.__len__()
    2
    >>> a.remove(4)
    >>> a.__len__()
    1
    """

    def __init__(self):
        super(SinglyLinkedList, self).__init__()
        self.head = None

    def __len__(self):
        myiter = self.__iter__()
        len = 0
        for item in myiter:
            len += 1
        return len

    def __iter__(self):
        node = self.head
        while node:
            yield node.item
            node = node.next

    def __contains__(self, item):
        items = self.__iter__()
        for data in items:
            if data == item:
                return True
        return False

    def remove(self, item):
        if self.head is None:
            print "Empty List. Cannot remove item!"
            return
        if self.__contains__(item) is True:
            prev = None
            cur = self.head
            while cur:
                if cur.item == item:
                    if prev:
                        prev.next = cur.next
                    else:
                        self.head = cur.next
                    return
                prev = cur
                cur = cur.next
        else:
            print"Item not found in the linked list!"

    def prepend(self, item):            # This method adds an item to the list.
        new_node = SinglyLinkedNode(item)
        new_node.next = self.head
        self.head = new_node

    def __repr__(self):
        s = "List:" + "->".join([repr(item) for item in self])
        return s


class ChainedHashDict(object):
    """
    >>> c=ChainedHashDict(5)            # Running the doctests
    >>> c[0]=1
    >>> c[2]=3
    >>> c[10]=4
    >>> print c.display()
    ***************************
    LENGTH:3
    BINS:5
    LOAD FACTOR:0.6
        0:List:10:4->0:1
        1:None
        2:List:2:3
        3:None
        4:None
    """
    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(ChainedHashDict, self).__init__()
        self._bin_count = bin_count
        self.table = [None] * bin_count
        self.len = 0
        self.hashfunc = hash
        self.max_load = max_load

    @property
    def load_factor(self):
        load = float(self.len) / len(self.table)
        return load

    @property
    def bin_count(self):
        return self._bin_count

    def rebuild(self, bincount):
        self.len = 0
        new_table = [None] * bincount
        for i in range(0, len(self.table)):
            if self.table[i]:
                myiter = self.table[i].__iter__()
                for item in myiter:
                    hashed = self.hashfunc(item.key) % bincount
                    if new_table[hashed] is None:
                        listed = SinglyLinkedList()
                        listed.prepend(item)
                        new_table[hashed] = listed
                    else:
                        new_table[hashed].prepend(item)
                    self.len += 1
        self.table = new_table

    def __getitem__(self, key):
        hashed = self.hashfunc(key) % len(self.table)

        myiter = self.table[hashed].__iter__()
        for item in myiter:
            if item.key == key:
                return item.value
        return "Value not found"

    def __setitem__(self, key, value):
        bins = len(self.table)
        flag = True
        kvpair = _KeyValuePair(key, value)
        hashed = self.hashfunc(key) % bins

        if self.table[hashed]:
            myiter = self.table[hashed].__iter__()
            for pair in myiter:
                if pair.key == key:
                    pair.value = value
                    flag = False
                    break
            if flag:
                self.table[hashed].prepend(kvpair)
        else:
            listed = SinglyLinkedList()
            listed.prepend(kvpair)
            self.table[hashed] = listed

        if flag:
            self.len += 1

        if self.load_factor > self.max_load:
            bins = bins * 2
            self.rebuild(bins)

    def __delitem__(self, key):
        bins = len(self.table)
        hashed = self.hashfunc(key) % bins
        if self.table[hashed]:
            myiter = self.table[hashed].__iter__()
            for item in myiter:
                if item.key == key:
                    if self.table[hashed].__len__() == 1:
                        self.table[hashed] = None
                    else:
                        self.table[hashed].remove(item)
                    self.len -= 1
                    return
        else:
            print "Value not found. could not delete"

    def __contains__(self, key):
        hashed = self.hashfunc(key) % len(self.table)
        myiter = self.table[hashed].__iter__()
        for item in myiter:
            if item.key == key:
                return True
        return False

    def __len__(self):
        return self.len

    def display(self):
        s = "***************************"
        s += "\nLENGTH:" + repr(self.len)
        s += "\n" + "BINS:" + repr(len(self.table))
        s += "\nLOAD FACTOR:" + repr(self.load_factor)+"\n"

        for i in range(0, len(self.table) - 1):
            s += "    " + repr(i) + ":" + repr(self.table[i]) + "\n"
        i += 1
        s += "    " + repr(i) + ":" + repr(self.table[i])
        return s


class _KeyValuePair(object):

    def __init__(self, key, value):
        super(_KeyValuePair, self).__init__()
        self.key = key
        self.value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @key.setter
    def key(self, key):
        self._key = key

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self):
        return repr(self.key) + ":" + repr(self.value)


class OpenAddressHashDict(object):
    """
    >>> e = OpenAddressHashDict(5, hashfunc = lambda x: int(x))
    >>> e[5] = 23
    >>> e[7] = 12
    >>> e[3] = 9
    >>> e.__delitem__(5)
    >>> e[1]=21
    >>> print e.display()
    ***************************
    LENGTH:3
    BINS:10
    LOAD FACTOR:0.3
      0: None
      1: 1:21
      2: None
      3: 3:9
      4: None
      5: None
      6: None
      7: 7:12
      8: None
      9: None
    """
    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(OpenAddressHashDict, self).__init__()
        self._bin_count = bin_count
        self.table = [None] * bin_count
        self.len = 0
        self.deleted = 0
        self.hashfunc = hash
        self.max_load = max_load

    @property
    def load_factor(self):
        load = float(self.len + self.deleted) / len(self.table)
        return load

    @property
    def bin_count(self):
        return self._bin_count

    def rebuild(self, bincount):
        self.len = 0
        self.deleted = 0

        new_table = [None] * bincount
        for i in range(0, len(self.table)):
            if self.table[i] and self.table[i] != "DELETED":
                j = 0
                while j < bincount:
                    index = (self.hashfunc(self.table[i].key) + j) % bincount
                    if new_table[index] is None:
                        self.len += 1
                        new_table[index] = self.table[i]
                        break
                    else:
                        j += 1
        self.table = new_table
        return

    def __getitem__(self, key):
        i = 0
        bins = len(self.table)
        while i != bins:
            hashed = (self.hashfunc(key) + i) % bins
            if self.table[hashed] and self.table[hashed] != "DELETED":
                if self.table[hashed].key == key:
                    return self.table[hashed].value
            i += 1
        return "Key not present in Hash Table"

    def __setitem__(self, key, value):
        bins = len(self.table)
        i = 0
        while i != bins:
            hashed = (self.hashfunc(key) + i) % bins
            if self.table[hashed] != "DELETED":
                if self.table[hashed] is None:
                    self.len += 1
                    pair = _KeyValuePair(key, value)
                    self.table[hashed] = pair
                    break
                elif self.table[hashed].key == key:
                    self.table[hashed].value = value
                    break
            i += 1
        if self.load_factor > self.max_load:
            bins = bins * 2
            self.rebuild(bins)

    def __delitem__(self, key):
        i = 0
        bins = len(self.table)
        while i != bins:
            hashed = (self.hashfunc(key) + i) % bins
            if self.table[hashed] and self.table[hashed] != "DELETED":
                if self.table[hashed].key == key:
                    self.table[hashed] = "DELETED"
                    self.len -= 1
                    self.deleted += 1
                    break
            i += 1

    def __contains__(self, key):
        i = 0
        bins = len(self.table)
        while i != bins:
            hashed = (self.hashfunc(key) + i) % bins
            if self.table[hashed] and self.table[hashed] != "DELETED":
                if self.table[hashed].key == key:
                    return True
                    break
            i += 1
        return False

    def __len__(self):
        return self.len

    def display(self):
        s = "***************************"
        s += "\nLENGTH:" + repr(self.len)
        s += "\n" + "BINS:" + repr(len(self.table))
        s += "\nLOAD FACTOR:" + repr(self.load_factor)+"\n"

        for i in range(0, len(self.table) - 1):
            s += "  " + repr(i) + ": " + repr(self.table[i]) + "\n"
        i += 1
        s += "  " + repr(i) + ": " + repr(self.table[i])
        return s


class BinaryTreeNode(object):
    def __init__(self, data=None, left=None, right=None, parent=None):
        super(BinaryTreeNode, self).__init__()
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent


class BinarySearchTreeDict(object):
    """
    >>> d = BinarySearchTreeDict()
    >>> d.__setitem__(4, 'A')
    >>> d.__setitem__(3, 'B')
    >>> d.__setitem__(7, 'C')
    >>> d.__setitem__(2, 'D')
    >>> d.__setitem__(9, 'E')
    >>> d.__setitem__(1, 'F')
    >>> d.__delitem__(7)
    Deleting the key..
    >>> d.__delitem__(2)
    Deleting the key..
    >>> d.__delitem__(9)
    Deleting the key..
    >>> d.__delitem__(1)
    Deleting the key..
    >>> d.__len__()
    The length of tree is : 2
    >>> d.display()
    Inorder traversal keys
    3 4 \n    Preorder traversal keys
    4 3 \n    Postorder traversal keys
    3 4
    """
    def __init__(self):
        super(BinarySearchTreeDict, self).__init__()
        self.root = None

    @property
    def height(self):
        q=Queue.Queue()
        if self.root:
            q.put(self.root)
        else:
            return 0
        height=-1
        while True:
            node_count=q.qsize()
            if node_count==0:
                return height
            height=height+1
            while node_count!=0:
                current_node=q.get()
                if current_node.left:
                    q.put(current_node.left)
                if current_node.right:
                    q.put(current_node.right)
                node_count=node_count-1

    def inorder_keys(self):

        x = self.root
        stack = []
        while x:
            while x.left:
                stack.append(x)
                x = x.left
            yield x.data.key
            while not x.right:
                if stack:
                    x = stack.pop()
                    yield x.data.key
                else:
                    return
            x = x.right

    def _peek(self, stack):
        if len(stack) == 0:
            return None
        else:
            return stack[len(stack) - 1]

    def postorder_keys(self):

        x = self.root
        if x is None:
            return
        stack = []
        while True:
            while x:
                if x.right:
                    stack.append(x.right)
                stack.append(x)
                x = x.left
            x = stack.pop()

            if x.right and self._peek(stack) == x.right:
                stack.pop()
                stack.append(x)
                x = x.right
            else:
                yield x.data.key
                x = None
            if len(stack) == 0:
                break

    def preorder_keys(self):

        x = self.root
        if x is None:
            return
        stack = []
        stack.append(x)
        while stack:
            x = stack.pop()
            yield x.data.key
            if x.right:
                stack.append(x.right)
            if x.left:
                stack.append(x.left)

    def items(self):
        keys = self.inorder_keys()
        for i in keys:
            yield i.item, i.value

    def __getitem__(self, key):

        x = self.root
        while x:
            if x.data.key == key:
                return x.data.value
            elif key < x.data.key:
                x = x.left
            elif key > x.data.key:
                x = x.right

    def __setitem__(self, key, value):
        y = None
        x = self.root
        pair = _KeyValuePair(key, value)
        z = BinaryTreeNode(pair, None, None, None)
        while x is not None:
            y = x
            if z.data.key < x.data.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is None:
            self.root = z
        elif z.data.key < y.data.key:
            y.left = z
        else:
            y.right = z

    def __treemin(self, key):
        x = self.root
        while x.left:
            x = x.left
        return x

    def __transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def __delitem__(self, key):
        print "Deleting the key.."
        x = self.root
        while x:
            if x.data.key == key:
                break
            elif key < x.data.key:
                x = x.left
            elif key > x.data.key:
                x = x.right

        if x is not None:
            if x.left is None:
                self.__transplant(x, x.right)
            elif x.right is None:
                self.__transplant(x, x.left)
            else:
                y = self.__treemin(x.right)
                if y.parent != x:
                    self.__transplant(y, y.right)
                    y.right = x.right
                    y.right.parent = y
                self.__transplant(x, y)
                y.left = x.left
                y.left.parent = y
        else:
            print "Key not found in the tree"

    def __contains__(self, key):
        x = self.root
        while x:
            if x.data.key == key:
                print " Item is present in the tree"
                return True
            elif key < x.data.key:
                x = x.left
            elif key > x.data.key:
                x = x.right
        print " Item is not present in the tree"

    def __len__(self):

        count = 0
        keys = self.inorder_keys()
        for i in keys:
            count = count + 1
        print "The length of tree is : %d" % count

    def display(self):

        keys = self.inorder_keys()
        print "Inorder traversal keys"
        for i in keys:
            print i,

        print "\nPreorder traversal keys"
        key1 = self.preorder_keys()
        for j in key1:
            print j,

        print "\nPostorder traversal keys"
        key2 = self.postorder_keys()
        for k in key2:
            print k,


def terrible_hash(bin):
    """A terrible hash function that can be used for testing.

    A hash function should produce unpredictable results,
    but it is useful to see what happens to a hash table when
    you use the worst-possible hash function.  The function
    returned from this factory function will always return
    the same number, regardless of the key.

    :param bin:
        The result of the hash function, regardless of which
        item is used.

    :return:
        A python function that can be passes into the constructor
        of a hash table to use for hashing objects.
    """
    def hashfunc(item):
        return bin
    return hashfunc


def main():
    # Thoroughly test your program and produce useful out.
    #
    # Do at least these kinds of tests:
    #  (1)  Check the boundary conditions (empty containers,
    #       full containers, etc)
    #  (2)  Test your hash tables for terrible hash functions
    #       that map to keys in the middle or ends of your
    #       table
    #  (3)  Check your table on 100s or randomly generated
    #       sets of keys to make sure they function
    #
    #  (4)  Make sure that no keys / items are lost, especially
    #       as a result of deleting another key
    print "***************Linked List IMPLEMENTATION***************"
    obj = SinglyLinkedList()

    obj.prepend(3)
    obj.prepend(5)
    obj.prepend(7)
    obj.prepend(9)
    obj.prepend(4)
    obj.prepend(6)
    obj.prepend(8)
    print obj.__repr__()
    obj.remove(9)
    print obj.__repr__()
    print obj.__len__()
    print obj.__contains__(3)

    print "\n***************Chained HASH IMPLEMENTATION***************"

    chained = ChainedHashDict(5)
    chained.__setitem__(0, 1)
    chained.__setitem__(2, 3)
    chained.__setitem__(10, 4)
    chained.__setitem__(7, 6)
    print chained.__getitem__(10)
    chained.__contains__(2)
    chained.__delitem__(7)
    print chained.__getitem__(10)
    print chained.display()

    print "\n***************Open Addresss HASH IMPLEMENTATION***************"

    open = OpenAddressHashDict(5, hashfunc=lambda x: int(x))
    open[5] = 23
    open[7] = 12
    open[3] = 9
    open.__delitem__(5)
    open[1] = 21

    print open.display()

    print "\n*************Binary Search Tree HASH IMPLEMENTATION*************"

    print "***BINARY SEARCH TREE***"
    t = BinarySearchTreeDict()
    t.__setitem__(4, 'A')
    t.__setitem__(3, 'B')
    t.__setitem__(2, 'C')
    t.__setitem__(9, 'D')
    t.__setitem__(5, 'E')
    t.__setitem__(10, 'F')
    t.__len__()
    t.inorder_keys()
    t.preorder_keys()
    t.postorder_keys()
    t.display()
    print "\nThe height of the tree is"
    print t.height

    print "TERRIBLE HASH"
    print "*************** Chained Terrible HASH ***************"
    chained1 = ChainedHashDict(10, hashfunc=terrible_hash(bin))
    for x in range(0, 10):
        y = random.randrange(0, 1000)
        chained1[y] = x
    print chained1.display()
    print "***************Open Address Terrible HASH ***************"
    open1 = OpenAddressHashDict(5, hashfunc=terrible_hash(bin))
    for x in range(0, 10):
        y = random.randrange(0, 1000)
        open1[y] = x
    print open1.display()

if __name__ == '__main__':
    main()
    import doctest
    doctest.testmod()
