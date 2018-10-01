#!/usr/bin/env python

import pytest
from app.doubly_linked_list import Node, DoublyLinkedList

class TestDoublyLinkedList:

    def setup(self):
        self.data = 1
        self.dll = DoublyLinkedList(Node(self.data))

    def test_size(self):
        self.setup()

        assert self.dll.size() == 1

    def test_get(self):
        self.setup()

        assert self.dll.get(0) == self.data

    def test_add(self):
        self.setup()

        assert self.dll.add(self.data) == True

    def test_remove(self):
        self.setup()

        assert self.dll.remove(self.data) == True

    def test_pop(self):
        self.setup()

        assert self.dll.pop() == self.data