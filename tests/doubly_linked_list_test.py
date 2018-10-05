#!/usr/bin/env python

import unittest
from app.double_linked_list import Item, DoubleLinkedList


class TestDoubleLinkedList(unittest.TestCase):

    def setUp(self):
        self.elements = [1, 2, 3]
        self.dll = DoubleLinkedList()

    def test_push(self):
        for element in self.elements:
            self.dll.push(element)
            self.assertEqual(element, self.dll.last())

    def test_pop(self):
        self.assertEqual(self.dll.pop(), None)

        self.test_push()
        for element in reversed(self.elements):
            self.assertEqual(self.dll.pop(), element)

    def test_is_empty(self):
        self.assertTrue(self.dll.is_empty())

    def test_unshift(self):
        element = 0
        self.dll.unshift(element)
        self.assertEqual(self.dll.first(), element)
        self.dll.delete(element)

        self.test_push()
        self.dll.unshift(element)
        self.assertEqual(self.dll.first(), element)
        self.assertEqual(self.dll.last(), self.elements[-1])

    def test_shift(self):
        self.assertEqual(self.dll.shift(), None)

        self.test_push()
        self.assertEqual(self.dll.shift(), self.elements[0])

    def test_len(self):
        self.assertEqual(self.dll.len(), 0)

        self.test_push()
        self.assertEqual(self.dll.len(), len(self.elements))

    def test_delete(self):
        self.assertEqual(self.dll.delete(None), None)

        self.test_push()
        for element in self.elements:
            self.assertEqual(self.dll.delete(element), element)

    def test_contains(self):
        self.test_push()

        self.assertTrue(self.dll.contains(self.elements[1]))
        self.assertFalse(self.dll.contains(None))

    def test_first(self):
        self.assertEqual(self.dll.first(), None)

        self.test_push()
        self.assertEqual(self.dll.first(), self.elements[0])

    def test_last(self):
        self.assertEqual(self.dll.last(), None)

        self.test_push()
        self.assertEqual(self.dll.last(), self.elements[-1])


if __name__ == "__main__":
    unittest.main()