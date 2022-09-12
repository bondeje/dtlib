# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 19:27:17 2022

@author: jeffr
"""

import dtlib.trees._ArrayOrderStatisticTree as AOST
import dtlib.trees._ArrayBinarySearchTree as ABST
import dtlib.trees._ArrayBinaryTree as ABT
import dtlib.trees._Node as _Node
from dtlib.trees._constants import DIR_PARENT, DIR_LEFT, DIR_RIGHT, \
    VALUE_KEY, TRAVERSE_GO, TRAVERSE_STOP, BT_BALANCED, \
    TRAVERSE_LEVELORDER, DEFAULT_SEARCH_ORDER, LIST_NODE, \
    WBT_ALPHA, _WBT_DOUBLEROT_THRESH
    
# TODO: create iterator classes for each type of iteration
# TODO: Iterable = AOST_iter(tree, /, *, traversal='inorder')

############################## Module globals ################################

## utilizing dtlib.trees._constants

SIZE_KEY = 1
DEFAULT_NODE_FACTORY = _Node.Node_factory(LIST_NODE, {SIZE_KEY: 1})

################################ UTILITIES ####################################

## comment out aliasing into namespace until they are actually needed. Left
## here for documentation purposes

_AWBT_is_leaf = AOST._AOST_is_leaf

_AWBT_move_index = ABT._ABT_move_index
_move = _AWBT_move_index

_AWBT_size = AOST._AOST_size

_AWBT_update_size = AOST._AOST_update_size

def _AWBT_balance(tree, index, /):
    if index >= len(tree) or tree[index] is None:
        return 0
    return (1 + _AWBT_size(tree, _move(index, DIR_LEFT))) / (1 + _AWBT_size(tree, index))

_AWBT_diameter = ABT._ABT_diameter

_AWBT_depth = ABT._ABT_depth

_AWBT_extend = ABT._ABT_extend

_AWBT_swap = ABT._ABT_swap

_AWBT_rotate = ABT._ABT_rotate

_AWBT_split_rotate = ABT._ABT_split_rotate

def _AWBT_rebalance(tree, _path, /):
    while _path >= 0:
        index = _path # now the last element, if present, is the parent of node
        # establishes parent--> child relationship in linked nodes; should not be necessary
        #if child is not None:
        #    node[dir_] = child
        
        bal_node = _AWBT_balance(tree, index)
        if bal_node < WBT_ALPHA:# unabalanced subtree; rotate left or double rotation
            # should be same as n->left->weight < alpha * n->weight in Brass p.64
            # but trying Blum's result...appears to work, but this is directly from Blum
            # note: Brass's doesn't make sense; a little worried it is ad-hoc with its secondary value epsilon (delta in Blum's paper)
            
            # if right child's balance is leq a threshold, single rotation else double rotation
            if _AWBT_balance(tree, _move(index, DIR_RIGHT)) <= _WBT_DOUBLEROT_THRESH:
                _AWBT_rotate(tree, index, DIR_LEFT)
                # establishes parent--> child relationship in linked nodes; should not be necessary
                #if _path: # update subtree's parent-child relationship if it exists
                #    _path[-1][0][_path[-1][1]] = child
                
                # update from affected children on up
                _AWBT_update_size(tree, _move(index, DIR_LEFT))
                _AWBT_update_size(tree, index)
            else:
                _AWBT_split_rotate(tree, index, DIR_LEFT)
                    
                # update from affected children on up
                _AWBT_update_size(tree, _move(index, DIR_RIGHT))
                _AWBT_update_size(tree, _move(index, DIR_LEFT))
                _AWBT_update_size(tree, index)
        elif bal_node > (1-WBT_ALPHA): # unbalanced subtree; rotate right or double rotation
            # should be same as n->right->weight < alpha * n->weight in Brass p.64
            # but trying Blum's result swapping right and left in definitions of child, grandchild
            # note: Brass's doesn't make sense; a little worried it is ad-hoc with its secondary value epsilon (delta in Blum's paper)
                                    
            # I'm not sure this makes sense...need to go through Blum's paper with reverse geometry
            # this makes sense in the sense that beta2 determines whether there are enough nodes in the grandchild subtree to warrant doulbe rotation and moving the grandchild up
            # this is what _AWBT_balance_child) for the rotate left condition does. The corresponding measure in the rotate right condition is 1-_AWBT_balance(child))
            # in any case, this passes a lot of randomized large tree building tests
            # if left child's balance is leq a threshold, single rotation else double rotation
            if 1 - _AWBT_balance(tree, _move(index, DIR_LEFT)) <= _WBT_DOUBLEROT_THRESH:
                _AWBT_rotate(tree, index, DIR_RIGHT)
                    
                # update affected subtree sizes
                _AWBT_update_size(tree, _move(index, DIR_RIGHT))
                _AWBT_update_size(tree, index) # update current subtree root
            else:
                _AWBT_split_rotate(tree, index, DIR_RIGHT)
                
                # update affected subtree sizes
                _AWBT_update_size(tree, _move(index, DIR_RIGHT))
                _AWBT_update_size(tree, _move(index, DIR_LEFT))
                _AWBT_update_size(tree, index)
        else: # node is already balanced
            pass
        _path = _move(_path, DIR_PARENT)
    return tree

_AWBT_move_subtree = ABT._ABT_move_subtree

_AWBT_leftmost = ABT._ABT_leftmost

_AWBT_rightmost = ABT._ABT_rightmost

_AWBT_search_most = ABST._ABST_search_most

_AWBT_search = ABST._ABST_search

_AWBT_select_N = AOST._AOST_select_N

################################# Traversals ##################################

## using the public API from ABT as the implementation is identical

################################# Public API ##################################

AWBT_create = AOST.AOST_create
## Tree properties/geometry

AWBT_size = _AWBT_size
AWBT_height = ABT.ABT_height
AWBT_depth = ABT.ABT_depth

## Tree contents/queries/traversals

AWBT_traverse = ABT.ABT_traverse

AWBT_search = ABST.ABST_search

AWBT_select = AOST.AOST_select

AWBT_rank = AOST.AOST_rank

AWBT_contains = ABST.ABST_contains

AWBT_min = ABST.ABST_min

AWBT_max = ABST.ABST_max
                
# CONSIDER: might be able to speed this up to O(k*logn) where k is the number of elements with the same value by utilizing _ABST_search
# WARNING: don't use this directly, subject to change signature; specifically the output
#ABST_find = ABT.ABT_find

# currently O(N)...could be faster
#TODO: need to update AOST_count to be the faster algorithm
AWBT_count = AOST.AOST_count

def AWBT_validate(tree, /, *, key=None, unique=False):
    result = [True]
    if key is None:
        def validate_node(tree, index, result):
            # left child
            child = _move(index, DIR_LEFT)
            if tree[child] is not None:
                if unique and tree[child] == tree[index]: # not unique
                    result[0] = False
                    return TRAVERSE_STOP
                elif tree[child][VALUE_KEY] > tree[index][VALUE_KEY]: # not sorted
                    result[0] = False
                    return TRAVERSE_STOP
            left_size = tree[child][SIZE_KEY]
            # right child
            child = _move(index, DIR_RIGHT)
            if tree[child] is not None:
                if unique and tree[child][VALUE_KEY] == tree[index][VALUE_KEY]: # not unique
                    result[0] = False
                    return TRAVERSE_STOP
                elif tree[child][VALUE_KEY] < tree[index][VALUE_KEY]: # not sorted
                    result[0] = False
                    return TRAVERSE_STOP
            if tree[index][SIZE_KEY] != 1 + left_size + tree[child][SIZE_KEY]:
                result[0] = False
                return TRAVERSE_STOP
            _balance = _AWBT_balance(tree, index)
            if _balance < WBT_ALPHA or _balance > (1-WBT_ALPHA):
                result[0] = False
                return TRAVERSE_STOP
            return TRAVERSE_GO
        AWBT_traverse(tree, validate_node, result, traversal=TRAVERSE_LEVELORDER)
    else:
        def validate_node(tree, index, result, key):
            # left child
            child = _move(index, DIR_LEFT)
            if tree[child] is not None:
                c = key(tree[child][VALUE_KEY])
                r = key(tree[index][VALUE_KEY])
                if unique and c == r: # not unique
                    result[0] = False
                    return TRAVERSE_STOP
                elif c > r: # not sorted
                    result[0] = False
                    return TRAVERSE_STOP
            left_size = tree[child][SIZE_KEY]
            # right child
            child = _move(index, DIR_RIGHT)
            if tree[child] is not None:
                c = key(tree[child][VALUE_KEY])
                r = key(tree[index][VALUE_KEY])
                if unique and c == r: # not unique
                    result[0] = False
                    return TRAVERSE_STOP
                elif c < r: # not sorted
                    result[0] = False
                    return TRAVERSE_STOP
            if tree[index][SIZE_KEY] != 1 + left_size + tree[child][SIZE_KEY]:
                result[0] = False
                return TRAVERSE_STOP
            _balance = _AWBT_balance(tree, index)
            if _balance < WBT_ALPHA or _balance > (1-WBT_ALPHA):
                result[0] = False
                return TRAVERSE_STOP
            return TRAVERSE_GO
        AWBT_traverse(tree, validate_node, result, key, traversal=TRAVERSE_LEVELORDER)
    return result[0]

def AWBT_add(tree, value, /, *, key=None, unique=False, update=False, node_factory=DEFAULT_NODE_FACTORY):
    path = []
    root = AOST.AOST_add(tree, value, key=key, unique=unique, update=update, node_factory=node_factory, path=path)
    return _AWBT_rebalance(path[-1]) # does not consume path
    
# TODO: ABST_update(tree_dest, *other_ABSTs, /, unique=False) # merge trees

def AWBT_remove(root, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER):
    path = []
    root = AOST.AOST_remove(root, value, key=key, order=order, path=path)
    return _AWBT_rebalance(path[-1]) # consumes path

#TODO need extensive modification...pull from ArrayWeightBalancedTree without _rebalance call
def AWBT_discard(tree, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER):
    try:
        return AWBT_remove(tree, value, key=key, order=order)
    except KeyError:
        return tree

