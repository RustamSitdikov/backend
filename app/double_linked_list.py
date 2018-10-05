#!/usr/bin/env python


class Item:
    """
    Doubly linked list's item implementation.
    """

    __slots__ = 'elem', 'prev__item', 'next__item'

    def __init__(self, elem=None, prev__item=None, next__item=None):
        self.elem = elem
        self.prev__item = prev__item
        self.next__item = next__item

    def __str__(self):
        return str(self.elem)


class DoubleLinkedList:
    """
    Doubly linked list implementation.
    """

    __slots__ = 'head', 'tail', 'count'

    def __init__(self, head=None):
        self.head = head
        self.tail = head
        self.count = 0 if self.head is None else 1

    def __str__(self):
        string = ""
        item = self.head
        while item is not None:
            string += str(item.elem)
            item = item.next__item
            if item:
                string += " -> "

        return string

    def push(self, elem):
        """
        Add a value to tail of list.
        :param elem: value to be added.
        :return:
        """

        item = Item(elem=elem)
        if self.head is None:
            self.head = item
            self.tail = self.head
        else:
            item.prev__item = self.tail
            self.tail.next__item = item
            self.tail = item

        self.count += 1

    def pop(self):
        """
        Remove a value from tail of list.
        :return: value removed from list.
        """

        if self.is_empty():
            return None

        item = self.tail
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev__item
            self.tail.next__item = None
        self.count -= 1

        return item.elem

    def is_empty(self):
        """
        Determine if list is empty.
        :return: True if list has no values.
        """

        return self.count == 0

    def unshift(self, elem):
        """
        Add a value to head of list.
        :param elem: value to be added.
        """

        self.head = Item(elem=elem, prev__item=None, next__item=self.head)
        if self.tail is None:
            self.tail = self.head
        self.count += 1

    def shift(self):
        """
        Remove a value from head of list.
        :return: head's value removed.
        """

        if self.is_empty():
            return None

        item = self.head
        self.head = self.head.next__item
        if self.head is not None:
            self.head.prev__item = None
        else:
            self.tail = None

        item.next__item = None
        self.count -= 1

        return item.elem

    def len(self):
        """
        Determine number of elements in list.
        :return: number of elements found in list.
        """

        return self.count

    def delete(self, elem):
        """
        Remove a value from list.
        :param elem: value to be removed.
        :return: value actually removed.
        """

        item = self.head
        while (item is not None) and (item.elem != elem):
            item = item.next__item
        if item is not None:
            if item.prev__item is not None:
                item.prev__item.next__item = item.next__item
            else:
                self.head = item.next__item

            if item.next__item is not None:
                item.next__item.prev__item = item.prev__item
            else:
                self.tail = item.prev__item

            self.count -= 1
            return item.elem

        return None

    def contains(self, elem):
        """
        Checks whether a value is within list.
        :param elem: value to be found in list.
        :return: True if value is in list.
        """

        item = self.head
        while (item is not None) and (item.elem != elem):
            item = item.next__item

        return item is not None

    def first(self):
        """
        Get a value of first item in list.
        :return: value of first item in list.
        """

        if self.head is None:
            return None

        return self.head.elem

    def last(self):
        """
        Get a value of last item in list.
        :return: value of last item in list.
        """

        if self.tail is None:
            return None

        return self.tail.elem


if __name__ == "__main__":
    pass
