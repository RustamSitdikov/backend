#!/usr/bin/env python

import unittest
from app.doubly_linked_list import Node, DoublyLinkedList


class TestDoublyLinkedList(unittest.TestCase):

    def setUp(self):
        self.data = 1
        self.count = 1
        self.dll = DoublyLinkedList(Node(self.data))

    def test_size(self):
        self.assertEqual(self.dll.size(), self.count)

    def test_get(self):
        self.assertEqual(self.dll.get(self.count - 1), self.data)

    def test_add(self):
        self.assertTrue(self.dll.add(self.data))

    def test_remove(self):
        self.assertTrue(self.dll.remove(self.data))

    def test_pop(self):
        self.assertEqual(self.dll.pop(), self.data)


if __name__ == "__main__":
    unittest.main()