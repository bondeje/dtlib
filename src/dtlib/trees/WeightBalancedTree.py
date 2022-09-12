# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 20:04:34 2022

@author: jeffr
"""

import dtlib.trees.OrderStatisticTree as OST
import dtlib.trees._ArrayWeightBalancedTree as AWBT
import dtlib.trees._LinkedWeightBalancedTree as LWBT
from dtlib.trees.Tree import Tree, TreeMeta
import dtlib.trees._Node as _Node

from dtlib.trees._constants import BT_BALANCED, TRAVERSE_INORDER, \
    LINKED_STORAGE, ARRAY_STORAGE, LIST_NODE, DEFAULT_SEARCH_ORDER, \
    SEARCH_FIRST_INORDER, SEARCH_LAST_INORDER, SEARCH_FIRST_LEVELORDER, \
    DIR_LEFT, DIR_RIGHT

## Public API/ABC for Binary Trees

## Really all this does is provide a selector/factory for Binary Tree implementations
## so that the public API is implementation independent

############################## Module globals ################################

## Creation/Types

DEFAULT_STORAGE = ARRAY_STORAGE
DEFAULT_LINKED_NODE_FACTORY = _Node.Node_factory(LIST_NODE, {DIR_LEFT: None, DIR_RIGHT: None, AWBT.SIZE_KEY: 1})
DEFAULT_ARRAY_NODE_FACTORY = _Node.Node_factory(LIST_NODE, {AWBT.SIZE_KEY: 1})

############################ Module Initialization ############################

# Think of this as an interface for BinarySearchTree
class WeightBalancedTree(OST.OrderStatisticTree, metaclass=TreeMeta):
    def __init__(self):
        self.name = "This is a Weight-Balanced Tree"
        
    def __new__(cls, *args, storage=DEFAULT_STORAGE, **kwargs):
        if storage == LINKED_STORAGE:
            inst = Tree.__new__(LinkedWeightBalancedTree, *args, **kwargs)
        elif storage == ARRAY_STORAGE:
            inst = Tree.__new__(ArrayWeightBalancedTree, *args, **kwargs)
        else:
            raise ValueError(f"storage mechanism {storage} for WeightBalancedTree creation not understood")
        return inst
    
    # eventually add select and rank though the implementations will be very slow compared to an OrderStatisticsTree

class LinkedWeightBalancedTree(OST.LinkedOrderStatisticTree, WeightBalancedTree):
    def __init__(self, contents=None, Nmin=0, /, *, inplace=False, binary_tree_type=BT_BALANCED, key=None, default_traverse=TRAVERSE_INORDER, unique=False, node_factory=DEFAULT_LINKED_NODE_FACTORY):
        # since initialization can be expensive for computation and memory and 
        # BinarySearchTrees initialize very differently from BinaryTrees, this
        # should not call BT.ArrayBinaryTree.__init__
        self.node_factory = node_factory
        if contents is None:
            self.tree = None
        else:
            self.tree = LWBT.LWBT_create(contents, binary_tree_type=binary_tree_type, node_factory=self.node_factory)
        self.key = key
        self._reversed = False
        self.default_traverse = default_traverse
        self.unique = unique
        self.name = "This is a Linked Order Statistic Tree"
    
    def validate(self):
        return LWBT.LWBT_validate(self.tree, key=self.default_key, unique=self.unique)
    
    def add(self, value, /):
        self.tree = LWBT.LWBT_add(self.tree, value, key=self.key, unique=self.unique, node_factory=self.node_factory)
    
    def remove(self, value, /, *, order=DEFAULT_SEARCH_ORDER):
        self.tree = LWBT.LWBT_remove(self.tree, value, key=self.key, order=order)
    
    def discard(self, value, /, *, order=DEFAULT_SEARCH_ORDER):
        self.tree = LWBT.LWBT_discard(self.tree, value, key=self.key, order=order)

class ArrayWeightBalancedTree(OST.ArrayOrderStatisticTree, WeightBalancedTree):
    def __init__(self, contents=None, Nmin=0, /, *, inplace=False, binary_tree_type=BT_BALANCED, key=None, default_traverse=TRAVERSE_INORDER, unique=False, node_factory=DEFAULT_ARRAY_NODE_FACTORY):
        # since initialization can be expensive for computation and memory and 
        # BinarySearchTrees initialize very differently from BinaryTrees, this
        # should not call BT.ArrayBinaryTree.__init__
        self.node_factory = node_factory
        if contents is None:
            self.tree = [None]*Nmin
        else:
            self.tree = AWBT.AWBT_create(contents, Nmin, inplace=inplace, binary_tree_type=binary_tree_type, node_factory=self.node_factory)
        self.key = key
        self._reversed = False
        self.default_traverse = default_traverse
        self.unique = unique
        self.name = "Array Order Statistic Tree" # TODO: remove once class hierarchy is stable
    
    def validate(self):
        return AWBT.AWBT_validate(self.tree, key=self.key, unique=self.unique)
    
    def add(self, value, /, update=False):
        self.tree = AWBT.AWBT_add(self.tree, value, key=self.key, unique=self.unique, update=update, node_factory=self.node_factory)
    
    def remove(self, value, /, *, order=DEFAULT_SEARCH_ORDER):
        self.tree = AWBT.AWBT_remove(self.tree, value, key=self.key, order=order)
    
    def discard(self, value, /, *, order=DEFAULT_SEARCH_ORDER):
        self.tree = AWBT.AWBT_discard(self.tree, value, key=self.key, order=order)