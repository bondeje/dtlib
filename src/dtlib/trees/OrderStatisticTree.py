# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 19:02:32 2022

@author: jeffr
"""

import abc
import dtlib.trees.BinarySearchTree as BST
import dtlib.trees._ArrayOrderStatisticTree as AOST
import dtlib.trees._LinkedOrderStatisticTree as LOST
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

DEFAULT_STORAGE = LINKED_STORAGE
DEFAULT_LINKED_NODE_FACTORY = _Node.Node_factory(LIST_NODE, {DIR_LEFT: None, DIR_RIGHT: None, LOST.SIZE_KEY: 1})
DEFAULT_ARRAY_NODE_FACTORY = _Node.Node_factory(LIST_NODE, {AOST.SIZE_KEY: 1})

############################ Module Initialization ############################

# Think of this as an interface for BinarySearchTree
class OrderStatisticTree(BST.BinarySearchTree, metaclass=TreeMeta):
    def __init__(self):
        self.name = "This is an Order Statistic Tree"
        
    def __new__(cls, *args, storage=DEFAULT_STORAGE, **kwargs):
        if storage == LINKED_STORAGE:
            inst = Tree.__new__(LinkedOrderStatisticTree, *args, **kwargs)
        elif storage == ARRAY_STORAGE:
            inst = Tree.__new__(ArrayOrderStatisticTree, *args, **kwargs)
        else:
            raise ValueError(f"storage mechanism {storage} for OrderStatisticsTree creation not understood")
        return inst
    
    # should inherit all requirements of BinaryTree plus it is searchable
    @abc.abstractmethod
    def select(self):
        pass
    
    @abc.abstractmethod
    def rank(self):
        pass
    
    # eventually add select and rank though the implementations will be very slow compared to an OrderStatisticsTree

class LinkedOrderStatisticTree(BST.LinkedBinarySearchTree, OrderStatisticTree):
    def __init__(self, contents=None, Nmin=0, /, *, inplace=False, binary_tree_type=BT_BALANCED, key=None, default_traverse=TRAVERSE_INORDER, unique=False, node_factory=DEFAULT_LINKED_NODE_FACTORY):
        # since initialization can be expensive for computation and memory and 
        # BinarySearchTrees initialize very differently from BinaryTrees, this
        # should not call BT.ArrayBinaryTree.__init__
        self.node_factory = node_factory
        if contents is None:
            self.tree = None
        else:
            self.tree = LOST.LOST_create(contents, binary_tree_type=binary_tree_type, node_factory=self.node_factory)
        self.key = key
        self._reversed = False
        self.default_traverse = default_traverse
        self.unique = unique
        self.name = "This is a Linked Order Statistic Tree"
    
    def select(self, k):
        return LOST.LOST_select(self.tree, k)
    
    def rank(self, value, /, *, order=DEFAULT_SEARCH_ORDER):
        return LOST.LOST_rank(self.tree, value, key=self.key, order=order)
    
    def validate(self):
        return LOST.LOST_validate(self.tree, key=self.default_key, unique=self.unique)
    
    def add(self, value, /):
        self.tree = LOST.LOST_add(self.tree, value, key=self.key, unique=self.unique, node_factory=self.node_factory)
    
    def remove(self, value, /, *, order=DEFAULT_SEARCH_ORDER):
        self.tree = LOST.LOST_remove(self.tree, value, key=self.key, order=order)
    
    def discard(self, value, /, *, order=DEFAULT_SEARCH_ORDER):
        self.tree = LOST.LOST_discard(self.tree, value, key=self.key, order=order)

class ArrayOrderStatisticTree(BST.ArrayBinarySearchTree, OrderStatisticTree):
    def __init__(self, contents=None, Nmin=0, /, *, inplace=False, binary_tree_type=BT_BALANCED, key=None, default_traverse=TRAVERSE_INORDER, unique=False, node_factory=DEFAULT_ARRAY_NODE_FACTORY):
        # since initialization can be expensive for computation and memory and 
        # BinarySearchTrees initialize very differently from BinaryTrees, this
        # should not call BT.ArrayBinaryTree.__init__
        self.node_factory = node_factory
        if contents is None:
            self.tree = [None]*Nmin
        else:
            self.tree = AOST.AOST_create(contents, Nmin, inplace=inplace, binary_tree_type=binary_tree_type, node_factory=self.node_factory)
        self.key = key
        self._reversed = False
        self.default_traverse = default_traverse
        self.unique = unique
        self.name = "Array Order Statistic Tree" # TODO: remove once class hierarchy is stable
    
    def select(self, k):
        return AOST.AOST_select(self.tree, k)
    
    def rank(self, value, /, *, order=DEFAULT_SEARCH_ORDER):
        return AOST.AOST_rank(self.tree, value, key=self.key, order=order)
    
    def validate(self):
        return AOST.AOST_validate(self.tree, key=self.key, unique=self.unique)
    
    def add(self, value, /, update=False):
        self.tree = AOST.AOST_add(self.tree, value, key=self.key, unique=self.unique, update=update, node_factory=self.node_factory)
    
    def remove(self, value, /, *, order=DEFAULT_SEARCH_ORDER):
        self.tree = AOST.AOST_remove(self.tree, value, key=self.key, order=order)
    
    def discard(self, value, /, *, order=DEFAULT_SEARCH_ORDER):
        self.tree = AOST.AOST_discard(self.tree, value, key=self.key, order=order)