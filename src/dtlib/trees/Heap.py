# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 20:22:53 2022

@author: jeffr
"""

import abc
import dtlib.trees.BinaryTree as BT
import dtlib.trees._ArrayHeap as AH
import dtlib.trees._LinkedHeap as LH
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
DEFAULT_LINKED_NODE_FACTORY = _Node.Node_factory(LIST_NODE, {DIR_LEFT: None, DIR_RIGHT: None})
DEFAULT_ARRAY_NODE_FACTORY = _Node.Node_factory(LIST_NODE)

############################ Module Initialization ############################

# Think of this as an interface for BinarySearchTree
class Heap(BT.BinaryTree, metaclass=TreeMeta):
    def __init__(self):
        self.name = "This is a Heap"
        
    def __new__(cls, *args, storage=DEFAULT_STORAGE, **kwargs):
        if storage == LINKED_STORAGE:
            inst = Tree.__new__(LinkedHeap, *args, **kwargs)
        elif storage == ARRAY_STORAGE:
            inst = Tree.__new__(ArrayHeap, *args, **kwargs)
        else:
            raise ValueError(f"storage mechanism {storage} for BinarySearchTree creation not understood")
        return inst
    
    # should inherit all requirements of BinaryTree plus it is searchable
    @abc.abstractmethod
    def minimum(self):
        pass
    
    @abc.abstractmethod
    def maximum(self):
        pass
    
    # eventually add select and rank though the implementations will be very slow compared to an OrderStatisticsTree

class LinkedHeap(BT.LinkedBinaryTree, Heap):
    def __init__(self, contents=None, Nmin=0, /, *, binary_tree_type=BT_BALANCED, key=None, default_traverse=TRAVERSE_INORDER, unique=False, node_factory=DEFAULT_LINKED_NODE_FACTORY):
        # since initialization can be expensive for computation and memory and 
        # BinarySearchTrees initialize very differently from BinaryTrees, this
        # should not call BT.ArrayBinaryTree.__init__
        self.node_factory = node_factory
        if contents is None:
            self.tree = None
        else:
            self.tree = LBST.LBST_create(contents, binary_tree_type=binary_tree_type, node_factory=self.node_factory)
        self.key = key
        self.default_traverse = default_traverse
        self.unique = unique
        self.name = "This is a Linked Heap"
    
    def minimum(self):
        return LBST.LBST_min(self.tree)
    
    def maximum(self):
        return LBST.LBST_max(self.tree)
    
    def validate(self):
        return LBST.LBST_validate(self.tree, key=self.default_key, unique=self.unique)
    
    def add(self, value, /):
        self.tree = LBST.LBST_add(self.tree, value, key=self.key, unique=self.unique, node_factory=self.node_factory)
    
    def remove(self, value, /, *, order=DEFAULT_SEARCH_ORDER):
        self.tree = LBST.LBST_remove(self.tree, value, key=self.key, order=order)
    
    def discard(self, value, /, *, order=DEFAULT_SEARCH_ORDER):
        self.tree = LBST.LBST_discard(self.tree, value, key=self.key, order=order)

class ArrayHeap(BT.ArrayBinaryTree, Heap):
    def __init__(self, contents=None, Nmin=0, /, *, inplace=False, binary_tree_type=BT_BALANCED, key=None, default_traverse=TRAVERSE_INORDER, unique=False, node_factory=DEFAULT_ARRAY_NODE_FACTORY):
        # since initialization can be expensive for computation and memory and 
        # BinarySearchTrees initialize very differently from BinaryTrees, this
        # should not call BT.ArrayBinaryTree.__init__
        self.node_factory = node_factory
        if contents is None:
            self.tree = [None]*Nmin
        else:
            self.tree = ABST.ABST_create(contents, Nmin, inplace=inplace, binary_tree_type=binary_tree_type, node_factory=self.node_factory)
        self.key = key
        self.default_traverse = default_traverse
        self.unique = unique
        self.name = "This is an Array Heap" # TODO: remove once class hierarchy is stable
    
    def minimum(self):
        return ABST.ABST_min(self.tree)
    
    def maximum(self):
        return ABST.ABST_max(self.tree)
    
    def validate(self):
        return ABST.ABST_validate(self.tree, key=self.key, unique=self.unique)
    
    def add(self, value, /, update=False):
        self.tree = ABST.ABST_add(self.tree, value, key=self.key, unique=self.unique, update=update, node_factory=self.node_factory)
    
    def remove(self, value, /, *, order=DEFAULT_SEARCH_ORDER):
        self.tree = ABST.ABST_remove(self.tree, value, key=self.key, order=order)
    
    def discard(self, value, /, *, order=DEFAULT_SEARCH_ORDER):
        self.tree = ABST.ABST_discard(self.tree, value, key=self.key, order=order)