# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 16:41:36 2022

@author: jeffr
"""

import abc

# allow arguments to pass to __new__ but not init to help select class instantiation
class TreeMeta(abc.ABCMeta):
    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args, **kwargs)
        if "storage" in kwargs:
            del kwargs["storage"]
        if isinstance(obj, cls):
            obj.__init__(*args, **kwargs)
        return obj

"""    
This is just a reference class that does not provide any functionality...yet
its main purpose is to provide a reference superclass from which each 
"interface" subtype of tree can actually create concrete subclasses, e.g. 
BinaryTree or BinarySearchTrees, although in the inheritance hierarchy are 
never directly instantiated
"""
#TODO: move a bunch of the abstractmethods from BinaryTree to Tree, but only
# if they apply to ALL trees and not just binary Trees, e.g. size, height, 
# depth
# if Tree ends up inheriting from some other object, should remove __new__
class Tree(metaclass=TreeMeta):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls) # clear up whatever args or keywords are passed.
    
    @abc.abstractmethod
    def size(self):
        pass
    
    def __len__(self):
        self.size()
        
    @abc.abstractmethod
    def add(self):
        pass
    
    @abc.abstractmethod
    def remove(self):
        pass
    
    @abc.abstractmethod
    def discard(self):
        pass