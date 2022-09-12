# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 18:56:19 2022

@author: jeffr
"""

import abc
from dtlib.trees._constants import BT_BALANCED, TRAVERSE_INORDER, \
    LINKED_STORAGE, ARRAY_STORAGE, LIST_NODE, DIR_LEFT, DIR_RIGHT
import dtlib.trees._ArrayBinaryTree as ABT
import dtlib.trees._LinkedBinaryTree as LBT
import dtlib.trees._Node as _Node
from dtlib.trees.Tree import Tree, TreeMeta

## Public API/ABC for Binary Trees

## Really all this does is provide a selector/factory for Binary Tree implementations
## so that the public API is implementation independent

############################## Module globals ################################

## Creation/Types

DEFAULT_STORAGE = LINKED_STORAGE
DEFAULT_LINKED_NODE_FACTORY = _Node.Node_factory(LIST_NODE, {DIR_LEFT: None, DIR_RIGHT: None})
DEFAULT_ARRAY_NODE_FACTORY = _Node.Node_factory(LIST_NODE)

############################ Module Initialization ############################

# Think of this as an interface for BinaryTree
#TODO: determine which of the abstractmethod really need to be here or should be pushed to Tree
class BinaryTree(Tree, metaclass=TreeMeta):
    def __init__(self):
        self.name = "This is a Binary Tree"
        
    def __new__(cls, *args, storage=DEFAULT_STORAGE, **kwargs):
        if storage == LINKED_STORAGE:
            inst = Tree.__new__(LinkedBinaryTree, *args, **kwargs)
        elif storage == ARRAY_STORAGE:
            inst = Tree.__new__(ArrayBinaryTree,*args, **kwargs)
        else:
            raise ValueError(f"storage mechanism {storage} for BinaryTree creation not understood")
        return inst
    
    @abc.abstractmethod
    def traverse(self):
        pass
    
    @abc.abstractmethod
    def iterator(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def __iter__(self):
        pass
        
    @abc.abstractmethod
    def count(self):
        pass
        
    """
    @abc.abstractmethod
    def find(self):
        pass
    """
    
    # highly suggest also implementing a more configurable version self.contains
    @abc.abstractmethod
    def __contains__(self):
        pass
    
    @abc.abstractmethod
    def __eq__(self):
        pass
    
    def __str__(self):
        return self.__format__('')
    
    def __format__(self, format_spec):
        return self.name
    
class LinkedBinaryTree(BinaryTree):
    def __init__(self, contents=None, /, *, binary_tree_type=BT_BALANCED, default_traverse=TRAVERSE_INORDER, key=None, node_factory=DEFAULT_LINKED_NODE_FACTORY):
        self.node_factory = node_factory
        self.tree = LBT.LBT_create(contents, binary_tree_type=binary_tree_type, node_factory=self.node_factory)
        self.key = key
        self._reversed = False
        self.default_traverse = default_traverse
        self.name = "Linked Binary Tree"
    
    def size(self):
        return LBT.LBT_size(self.tree)
    
    def traverse(self, func, *args, traversal=None, reverse=None, **kwargs):
        if traversal is None:
            traversal = self.default_traverse
        if reverse is None:
            reverse = self._reverse
        elif reverse:
            reverse = not self._reversed
        LBT.LBT_traverse(self.tree, func, *args, traversal=traversal, reverse=reverse, **kwargs)
    
    def reverse(self):
        self._reversed = not self._reversed
    
    def iterator(self, order=None, /):
        if order is None:
            return self.__iter__()
        
        #TODO: see notes at top
        raise NotImplementedError(f"iterator by {order} is not yet implemented")
    
    def __reversed__(self):
        raise NotImplementedError("reverse iterator not yet implemented")
    
    def __iter__(self):
        #TODO: see notes at top
        raise NotImplementedError("iterator is not yet implemented")
        
    """ for a future release where something other than self.key can be used
    def count(self, value, /, *, key=None):
        if key is None:
            key = self.key
        return LBT.LBT_count(self.tree, value, key=key)
    """
    def count(self, value, /):
        return LBT.LBT_count(self.tree, value, key=self.key)
    
    """ # WARNING: don't use this. Need to review the signature; specifically the output
    def find(self, value, number=-1, /, *, key=None):
        if key is None:
            key = self.default_key
        return LBT._LBT_find(self.tree, value, number=number, key=key)
    """
    
    # highly suggest also implementing a more configurable version self.contains
    """ for a future release where something other than self.key can be used
    def __contains__(self, value, /, *, key=None): 
        if key is None:
            key = self.key
        return LBT.LBT_contains(self.tree, value, key=key)
    """
    def __contains__(self, value, /): 
        return LBT.LBT_contains(self.tree, value, key=self.key)
    
    def add(self, value, /):
        self.tree = LBT.LBT_add(self.tree, value)
    
    """ for a future release where something other than self.key can be used
    def remove(self, value, /, *, key=None):
        if key is None:
            key = self.key
        self.tree = LBT.LBT_remove(self.tree, value, key=key)
    """
    def remove(self, value, /):
        self.tree = LBT.LBT_remove(self.tree, value, key=self.key)
    
    """ for a future release where something other than self.key can be used
    def discard(self, value, /, *, key=None):
        if key is None:
            key = self.key
        self.tree = LBT.LBT_discard(self.tree, value, key=key)
    """
    def discard(self, value, /):
        self.tree = LBT.LBT_discard(self.tree, value, key=self.key)
    
    def __eq__(self, other, /):
        return LBT.LBT_equals(self.tree, other)
    
class ArrayBinaryTree(BinaryTree):
    def __init__(self, contents=None, Nmin=0, /, *, inplace=False, binary_tree_type=BT_BALANCED, key=None, default_traverse=TRAVERSE_INORDER, node_factory=DEFAULT_ARRAY_NODE_FACTORY):
        self.tree = ABT.ABT_create(contents, Nmin, inplace=inplace, binary_tree_type=binary_tree_type)
        self.key = key
        self._reversed = False
        self.node_factory = node_factory
        self.default_traverse = default_traverse
        self.name = "Array Binary Tree" # TODO: remove once class hierarchy is stable
        
    def size(self):
        return ABT.ABT_size(self.tree)
    
    def traverse(self, func, *args, traversal=None, reverse=None, **kwargs):
        if traversal is None:
            traversal = self.default_traverse
        if reverse is None:
            reverse = self._reverse
        elif reverse:
            reverse = not self._reversed
        ABT.ABT_traverse(self.tree, func, *args, traversal=traversal, reverse=reverse, **kwargs)
        
    def reverse(self):
        self._reversed = not self._reversed
    
    def iterator(self, order=None, /):
        if order is None:
            return self.__iter__()
        #TODO: see notes at top
        raise NotImplementedError(f"iterator by {order} is not yet implemented")
    
    def __reversed__(self):
        raise NotImplementedError("reverse iterator not yet implemented")
    
    def __iter__(self):
        #TODO: see notes at top
        raise NotImplementedError("iterator is not yet implemented")
        
    """ for a future release where something other than self.key can be used
    def count(self, value, /, *, key=None):
        if key is None:
            key = self.key
        return ABT.ABT_count(self.tree, value, key=key)
    """
    def count(self, value, /):
        return ABT.ABT_count(self.tree, value, key=self.key)
    
    """ # WARNING: don't use this. Need to review the signature; specifically the output    
    def find(self, value, number=-1, /, *, key=None):
        if key is None:
            key = self.key
        return ABT.ABT_find(self.tree, value, number=number, key=key)
    """
    
    # highly suggest also implementing a more configurable version self.contains
    """ for a future release where something other than self.key can be used
    def __contains__(self, value, /, *, key=None): 
        if key is None:
            key = self.key
        return ABT.ABT_contains(self.tree, value, key=key)
    """
    def __contains__(self, value, /): 
        return ABT.ABT_contains(self.tree, value, key=self.key)
    
    def add(self, value, /):
        self.tree = ABT.ABT_add(self.tree, value, node_factory=self.node_factory)
    
    """ for a future release where something other than self.key can be used
    def remove(self, value, /, *, key=None):
        if key is None:
            key = self.key
        self.tree = ABT.ABT_remove(self.tree, value, key=key)
    """
    def remove(self, value, /):
        self.tree = ABT.ABT_remove(self.tree, value, key=self.key)
    
    """ for a future release where something other than self.key can be used
    def discard(self, value, /, *, key=None):
        if key is None:
            key = self.key
        self.tree = ABT.ABT_discard(self.tree, value, key=key)
    """
    def discard(self, value, /):
        self.tree = ABT.ABT_discard(self.tree, value, key=self.key)
    
    def __eq__(self, other, /):
        return ABT.ABT_equals(self.tree, other)