# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 23:23:16 2022

@author: jeffr
"""

import dtlib.trees._Node as _Node
from dtlib.trees._constants import DIR_LEFT, DIR_RIGHT, VALUE_KEY
from unittest import TestCase as TC

class cd():
    def __init__(self, a):
        self.a = a

class test_Node(TC):
    @classmethod
    def setUpClass(cls):
        cls.node_data = [[0, 1, 2],
                         [(0,), (1,), (2,)],
                         [[0],[1], [2]],
                         [{'a':0}, {'a':1}, {'a': 2}],
                         [cd(0), cd(1), cd(2)]]
        cls.node_type_consts = [_Node.LIST_NODE, _Node.DICT_NODE, _Node.CLASS_NODE, _Node.SLOTTED_CLASS_NODE]
        cls.node_types = [list, dict, _Node.ClassNode, _Node.SlottedClassNode]
    
    def test_NodeObjects(self):
        for i, node_type in enumerate(self.node_type_consts):
            node_factory = _Node.Node_factory(node_type, {DIR_LEFT: None, DIR_RIGHT: None})
            for data in self.node_data:
                root = node_factory(data[0], node_factory(data[1]), node_factory(data[2]))
                self.assertIsInstance(root, self.node_types[i])
                self.assertIsNotNone(root[DIR_LEFT])
                self.assertIsNotNone(root[DIR_RIGHT])
                self.assertEqual(data[0], root[VALUE_KEY])
                self.assertIsInstance(root[DIR_LEFT], self.node_types[i])
                self.assertIsNone(root[DIR_LEFT][DIR_LEFT])
                self.assertIsNone(root[DIR_LEFT][DIR_RIGHT])
                self.assertEqual(data[1], root[DIR_LEFT][VALUE_KEY])
                self.assertIsInstance(root[DIR_RIGHT], self.node_types[i])
                self.assertIsNone(root[DIR_RIGHT][DIR_LEFT])
                self.assertIsNone(root[DIR_RIGHT][DIR_RIGHT])
                self.assertEqual(data[2], root[DIR_RIGHT][VALUE_KEY])