# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 19:27:29 2022

@author: jeffr
"""

import dtlib.trees._LinkedOrderStatisticTree as LOST
import dtlib.trees._LinkedBinarySearchTree as LBST
import dtlib.trees._LinkedBinaryTree as LBT
import dtlib.trees._Node as _Node
from dtlib.trees._constants import DIR_LEFT, DIR_RIGHT, \
    VALUE_KEY, TRAVERSE_GO, TRAVERSE_STOP, BT_BALANCED, \
    TRAVERSE_LEVELORDER, DEFAULT_SEARCH_ORDER, LIST_NODE, \
    WBT_ALPHA, _WBT_DOUBLEROT_THRESH
    
# TODO: create iterator classes for each type of iteration
# TODO: Iterable = LOST_iter(tree, /, *, traversal='inorder')

############################## Module globals ################################

## utilizing BLib.Trees._constants

SIZE_KEY = 3
DEFAULT_NODE_FACTORY = _Node.Node_factory(LIST_NODE, {DIR_LEFT: None, DIR_RIGHT: None, SIZE_KEY: 1})

################################ UTILITIES ####################################

## comment out aliasing into namespace until they are actually needed. Left
## here for documentation purposes

_LWBT_is_leaf = LOST._LOST_is_leaf

_LWBT_size = LOST._LOST_size

_LWBT_update_size = LOST._LOST_update_size

def _LWBT_balance(node, /):
    if node is None:
        return 0
    return (1 + _LWBT_size(node[DIR_LEFT]))/(1 + _LWBT_size(node))

_LWBT_diameter = LBT._LBT_diameter

_LWBT_depth = LBT._LBT_depth

_LWBT_swap = LBT._LBT_swap

_LWBT_rotate = LBT._LBT_rotate

def _LWBT_rebalance(_path, /):
    child = None # must set to None for initial loop
    dir_ = None
    while _path:
        node = _path.pop() # now the last element, if present, is the parent of node
        
        # establishes parent--> child relationship in linked nodes
        if child is not None:
            node[dir_] = child
        # This next line should replace the need to have an explicit direction in the path
        dir_ = DIR_RIGHT if _path and _path[-1][DIR_RIGHT] is node else DIR_LEFT
        
        bal_node = _LWBT_balance(node)
        if bal_node < WBT_ALPHA:# unabalanced subtree; rotate left or double rotation
            # should be same as n->left->weight < alpha * n->weight in Brass p.64
            # but trying Blum's result...appears to work, but this is directly from Blum
            # note: Brass's doesn't make sense; a little worried it is ad-hoc with its secondary value epsilon (delta in Blum's paper)
            
            child = node[DIR_RIGHT]
            
            # if child's balance is leq a threshold, single rotation else double rotation
            if _LWBT_balance(child) <= _WBT_DOUBLEROT_THRESH:
                child = _LWBT_rotate(node, DIR_LEFT)
                if _path: # update subtree's parent-child relationship if it exists
                    _path[-1][0][_path[-1][1]] = child
                
                _LWBT_update_size(child[DIR_LEFT]) # update original node
                _LWBT_update_size(child) # update current subtree root
            else:
                child = _LWBT_rotate(child, DIR_RIGHT)
                node[DIR_RIGHT] = child
                child = _LWBT_rotate(node, DIR_LEFT)
                if _path: # update subtree's parent-child relationship if it exists
                    _path[-1][0][_path[-1][1]] = child
                    
                # update affected subtree sizes
                _LWBT_update_size(child[DIR_RIGHT])
                _LWBT_update_size(child[DIR_LEFT])
                _LWBT_update_size(child)
        elif bal_node > (1-WBT_ALPHA): # unbalanced subtree; rotate right or double rotation
            # should be same as n->right->weight < alpha * n->weight in Brass p.64
            # but trying Blum's result swapping right and left in definitions of child, grandchild
            # note: Brass's doesn't make sense; a little worried it is ad-hoc with its secondary value epsilon (delta in Blum's paper)
            
            child = node[DIR_LEFT]
                        
            # I'm not sure this makes sense...need to go through Blum's paper with reverse geometry
            # this makes sense in the sense that beta2 determines whether there are enough nodes in the grandchild subtree to warrant doulbe rotation and moving the grandchild up
            # this is what _LWBT_balance_child) for the rotate left condition does. The corresponding measure in the rotate right condition is 1-_LWBT_balance(child))
            # in any case, this passes a lot of randomized large tree building tests
            # if child's balance is leq a threshold, single rotation else double rotation
            if 1 - _LWBT_balance(child) <= _WBT_DOUBLEROT_THRESH:
                child = _LWBT_rotate(node, DIR_RIGHT)
                if _path: # update subtree's parent-child relationship if it exists
                    _path[-1][0][_path[-1][1]] = child
                    
                # update affected subtree sizes
                _LWBT_update_size(child[DIR_RIGHT]) # update original node
                _LWBT_update_size(child) # update current subtree root
            else:
                child = _LWBT_rotate(child, DIR_LEFT)
                node[DIR_LEFT] = child
                child = _LWBT_rotate(node, DIR_RIGHT)
                if _path: # update subtree's parent-child relationship if it exists
                    _path[-1][0][_path[-1][1]] = child
                
                # update affected subtree sizes
                _LWBT_update_size(child[DIR_LEFT])
                _LWBT_update_size(child[DIR_RIGHT])
                _LWBT_update_size(child) # set child to current subtree root
        else: # node is already balanced
            child = node # set child to current subtree root
                
    # if path is empty, child should be the last subtree root and therefore the new root
    return child

_LWBT_leftmost = LBT._LBT_leftmost

_LWBT_rightmost = LBT._LBT_rightmost

_LWBT_search_most = LBST._LBST_search_most

_LWBT_search = LBST._LBST_search

_LWBT_select_N = LOST._LOST_select_N

################################# Traversals ##################################

## using the public API from ABT as the implementation is identical

################################# Public API ##################################

LWBT_create = LOST.LOST_create

## Tree properties/geometry

LWBT_size = LOST._LOST_size
LWBT_height = LBT.LBT_height
LWBT_depth = LBT.LBT_depth

## Tree contents/queries/traversals

LWBT_traverse = LBT.LBT_traverse

LWBT_search = LBST.LBST_search

LWBT_select = LOST.LOST_select

LWBT_rank = LOST.LOST_rank

LWBT_contains = LBST.LBST_contains

LWBT_min = LBST.LBST_min

LWBT_max = LBST.LBST_max

# currently O(N)...could be faster
#TODO: need to update LOST_count to be the faster algorithm
LWBT_count = LOST.LOST_count

def LWBT_validate(root, /, *, key=None, unique=False):
    result = [True]
    if key is None:
        def validate_node(st, node, result):
            # left child
            child = node[DIR_LEFT]
            if child is not None:
                if unique and child[VALUE_KEY] == node[VALUE_KEY]: # not unique
                    result[0] = False
                    return TRAVERSE_STOP
                elif child[VALUE_KEY] > node[VALUE_KEY]: # not sorted
                    result[0] = False
                    return TRAVERSE_STOP
            left_size = child[SIZE_KEY]
            # right child
            child = node[DIR_RIGHT]
            if child is not None:
                if unique and child[VALUE_KEY] == node[VALUE_KEY]: # not unique
                    result[0] = False
                    return TRAVERSE_STOP
                elif child[VALUE_KEY] < node[VALUE_KEY]: # not sorted
                    result[0] = False
                    return TRAVERSE_STOP
            if node[SIZE_KEY] != 1 + left_size + child[SIZE_KEY]:
                result[0] = False
                return TRAVERSE_STOP
            _balance = _LWBT_balance(node)
            if _balance < WBT_ALPHA or _balance > (1-WBT_ALPHA):
                result[0] = False
                return TRAVERSE_STOP
            return TRAVERSE_GO
        LWBT_traverse(root, validate_node, result, traversal=TRAVERSE_LEVELORDER)
    else:
        def validate_node(st, node, result, key):
            # left child
            child = node[DIR_LEFT]
            if child is not None:
                c = key(child[VALUE_KEY])
                r = key(node[VALUE_KEY])
                if unique and c == r: # not unique
                    result[0] = False
                    return TRAVERSE_STOP
                elif c > r: # not sorted
                    result[0] = False
                    return TRAVERSE_STOP
            left_size = child[SIZE_KEY]
            # right child
            child = node[DIR_RIGHT]
            if child is not None:
                c = key(child[VALUE_KEY])
                r = key(node[VALUE_KEY])
                if unique and c == r: # not unique
                    result[0] = False
                    return TRAVERSE_STOP
                elif c < r: # not sorted
                    result[0] = False
                    return TRAVERSE_STOP
            if node[SIZE_KEY] != 1 + left_size + child[SIZE_KEY]:
                result[0] = False
                return TRAVERSE_STOP
            _balance = _LWBT_balance(node)
            if _balance < WBT_ALPHA or _balance > (1-WBT_ALPHA):
                result[0] = False
                return TRAVERSE_STOP
            return TRAVERSE_GO
        LWBT_traverse(root, validate_node, result, key, traversal=TRAVERSE_LEVELORDER)
    return result[0]

#TODO: I am here in updating

def LWBT_add(root, value, /, *, key=None, unique=False, update=False, node_factory=DEFAULT_NODE_FACTORY):
    path = []
    root = LOST.LOST_add(root, value, key=key, unique=unique, update=update, node_factory=node_factory, path=path)
    return _LWBT_rebalance(path) # consumes path
    
# TODO: ABST_update(tree_dest, *other_ABSTs, /, unique=False) # merge trees

def LWBT_remove(root, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER):
    path = []
    root = LOST.LOST_remove(root, value, key=key, order=order, path=path)
    return _LWBT_rebalance(path) # consumes path

#TODO need extensive modification...pull from ArrayWeightBalancedTree without _rebalance call
def LWBT_discard(root, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER):
    try:
        return LWBT_remove(root, value, key=key, order=order)
    except KeyError:
        return root

