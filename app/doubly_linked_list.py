#!/usr/bin/env python

class Node:
    """
    Doubly linked list's node implementation.
    """

    def __init__(self, data=None, previous=None, next=None):
        self.data = data
        self.previous = previous
        self.next = next

    def __str__(self):
        return str(self.data)

class DoublyLinkedList:
    """
    Doubly linked list implementation.
    """

    def __init__(self, head=None):
        self.head = head
        self.tail = head

        self.count = 0 if self.head is None else 1

    def size(self):
        node = self.head
        size = 0
        while node is not None:
            size += 1
            node = node.next
        return size

    def get(self, index):
        i = 0
        node = self.head
        while node is not None:
            if index == i:
                return node.data
            i += 1
            node = node.next

        return None

    def add(self, data):
        node = Node(data)

        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.previous = self.tail
            self.tail.next = node
            self.tail = node

        self.count += 1

        return True

    def remove(self, data):
        node = self.head
        while node is not None:
            if node.data == data:
                if node.previous is not None:
                    node.previous.next = node.next

                if node.next is not None:
                    node.next.previous = node.previous

                if node.data == self.head.data:
                    self.head = node.next

                if node.data == self.tail.data:
                    self.tail = node.previous

                self.count -= 1
                return True

            node = node.next

        return False

    def pop(self):
        tail = self.tail
        if tail is not None:
            previous = self.tail.previous
            if previous is not None:
                previous.next = None
            self.tail = previous
        else:
            tail = self.head
            self.head = None

        self.count -= 1

        return tail.data

    def __str__(self):
        string = ""
        node = self.head
        while node is not None:
            string += str(node.data)
            node = node.next
            if node:
                string += " -> "
        return string

    def __len__(self):
        return self.count


if __name__ == "__main__":
    doublyLinkedList = DoublyLinkedList()
    doublyLinkedList.add(1)
    doublyLinkedList.add("two")
    doublyLinkedList.add("three")

    print(doublyLinkedList)

    assert doublyLinkedList.size() == 3

    assert doublyLinkedList.pop() == "three"
    assert doublyLinkedList.pop() == "two"
    assert doublyLinkedList.pop() == 1
