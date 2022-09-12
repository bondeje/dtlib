# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 21:25:36 2022

@author: jeffr
"""

############################## Package globals ################################

## Creation/Construction

LIST_NODE = 'l'
DICT_NODE = 'd'
CLASS_NODE = 'c'
SLOTTED_CLASS_NODE = 'cs'

BT_BALANCED = 0
BT_COMPLETE = 1

LINKED_STORAGE = 'Linked'
ARRAY_STORAGE = 'Array'

## Navigation

# Whereas most of the other globals are just identifiers for algorithm or 
# structure selection, these are used as list indices and constants in
# algorithms. DO NOT CHANGE THESE
DIR_PARENT = -1
VALUE_KEY = 0
DIR_LEFT = 1
DIR_RIGHT = 2

## Traversals

TRAVERSE_STOP = False
TRAVERSE_GO = True

TRAVERSE_INORDER = 0
TRAVERSE_PREORDER = 1
TRAVERSE_POSTORDER = 2
TRAVERSE_LEVELORDER = 3

## BST

SEARCH_FIRST_INORDER = -1
SEARCH_FIRST_LEVELORDER = 0
SEARCH_LAST_INORDER = 1
DEFAULT_SEARCH_ORDER = SEARCH_FIRST_LEVELORDER

## Weight-Balanced Tree

WBT_ALPHA = 1-2**.5/2 # 2/11 < WBT_ALPHA < 1-sqrt(2)/2 - c(WBT_DELTA) # C(WBT_DELTA) defined in Blum, but we know c(0) = 0 

# don't change this. Proof of upper bound in Nievergelt, Proof of lower bound in Blum
assert 2/11 <= WBT_ALPHA <= 1-2**.5/2
WBT_DELTA = 0 # must be between 0 and 0.01; would prefer an analytic formula but have to follow Blum to identify, 0 corresponds to Nievergelt
_WBT_DOUBLEROT_THRESH = 1./(2-WBT_ALPHA) + WBT_DELTA/((1+(1+WBT_DELTA)*(1-WBT_ALPHA))*(2-WBT_ALPHA))