# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 13:32:25 2022

@author: jeffr
"""

from collections.abc import Iterable
import dtlib.trees._ArrayBinaryTree as ABT
import dtlib.trees._Node as _Node
from dtlib.trees._constants import VALUE_KEY, DIR_LEFT, DIR_RIGHT, \
    TRAVERSE_GO, TRAVERSE_STOP, BT_BALANCED,\
    TRAVERSE_LEVELORDER, SEARCH_FIRST_INORDER, \
    SEARCH_LAST_INORDER, DEFAULT_SEARCH_ORDER, LIST_NODE
from operator import gt, lt
    
# TODO: create iterator classes for each type of iteration
# TODO: Iterable = ABST_iter(tree, /, *, traversal='inorder')

############################## Module globals ################################

## utilizing BLib.Trees._constants

DEFAULT_NODE_FACTORY = _Node.Node_factory(LIST_NODE)

################################ UTILITIES ####################################

## comment out aliasing into namespace until they are actually needed. Left
## here for documentation purposes

_ABST_is_leaf = ABT._ABT_is_leaf

_ABST_move_index = ABT._ABT_move_index
_move = _ABST_move_index

_ABST_size = ABT.ABT_size

_ABST_diameter = ABT._ABT_diameter

_ABST_depth = ABT._ABT_depth

_ABST_extend = ABT._ABT_extend

_ABST_swap = ABT._ABT_swap

_ABST_move_subtree = ABT._ABT_move_subtree

_ABST_leftmost = ABT._ABT_leftmost

_ABST_rightmost = ABT._ABT_rightmost

# specicalization of _ABST_search. key(tree[index][VALUE_KEY]) == key(value) or tree[index][VALUE_KEY] == value must be satisfied
def _ABST_search_most(tree, index, dir_, /, *, key=None, path=None):
    if path is None:
        path = []
    if dir_ == DIR_LEFT:
        _leader, _follower, cmp = DIR_LEFT, DIR_RIGHT, lt
    else:
        _leader, _follower, cmp = DIR_RIGHT, DIR_LEFT, gt
    #most = index
    N = len(tree)
    if key is None:
        value = tree[index][VALUE_KEY]
        while index < N and tree[index] is not None:
            kindex = tree[index][VALUE_KEY]
            if kindex == value:
                path.append(index)
                #most = index
                index = _move(index, _leader)
            elif cmp(kindex, value): # was kindex < value for _ABST_search_leftmost
                path.append(index)
                index = _move(index, _follower)
            else:
                index = N # exit condition
                #return most
        while tree[path[-1]][VALUE_KEY] != value:
            path.pop()
    else:
        value = key(tree[index][VALUE_KEY])
        while index < N and tree[index] is not None:
            kindex = key(tree[index][VALUE_KEY])
            if kindex == value:
                path.append(index)
                #most = index
                index = _move(index, _leader)
            elif cmp(kindex, value): # was kindex < value for _ABST_search_leftmost
                path.append(index)
                index = _move(index, _follower)
            else:
                index = N # exit condition
                #return most
        while key(tree[path[-1]][VALUE_KEY]) != value:
            path.pop()
    #return most
    return path[-1]

# TODO: find a way to inject uniqueness into the search; otherwise the leftmost and rightmost are triggered and full O(height) is computed
def _ABST_search(tree, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER, path=None):
    if path is None:
        path = []
    root = 0
    N = len(tree)
    if key is None:
        while root < N and tree[root] is not None:
            path.append(root)
            cur = tree[root][VALUE_KEY]
            if cur == value:
                break # continue with root
            elif cur < value:
                root = _move(root, DIR_RIGHT)
            else:
                root = _move(root, DIR_LEFT)
    else:
        while root < N and tree[root] is not None:
            path.append(root)
            cur = key(tree[root][VALUE_KEY])
            if cur == value:
                break # continue with root
            elif cur < value:
                root = _move(root, DIR_RIGHT)
            else:
                root = _move(root, DIR_LEFT)
    
    if root < N and tree[root] is not None:
        if order == SEARCH_FIRST_INORDER:
            path.pop()
            root = _ABST_search_most(tree, root, DIR_LEFT, key=key, path=path)
            #root = _ABST_search_leftmost(tree, root, key=key)
        elif order == SEARCH_LAST_INORDER:
            path.pop()
            root = _ABST_search_most(tree, root, DIR_RIGHT, key=key, path=path)
            #root = _ABST_search_rightmost(tree, root, key=key)
        else: # order == SEARCH_FIRST_LEVELORDER
            pass
    return root

################################# Traversals ##################################

## using the public API from ABT as the implementation is identical

################################# Public API ##################################

# node_factory is only meant for specializations that actually requires nodes. For simple BSTs, do not use node_factory unless you correct the key parameters for the node structure
def ABST_create(contents=None, Nmin=0, /, *, key=None, inplace=False, binary_tree_type=BT_BALANCED, node_factory=None):
    if contents is None:
        return [None]*Nmin
    
    if isinstance(contents, Iterable):
        if inplace:
            if not isinstance(contents, list):
                raise ValueError("cannot create an ABT in place with non-list contents")
            else:
                contents.sort(key=key)
        else:
            contents = sorted(contents, key=key)
    else:
        contents = [contents]
        
    return ABT.ABT_create(contents, Nmin, inplace=inplace, binary_tree_type=binary_tree_type, node_factory=node_factory)
    
## Tree properties/geometry

ABST_size = ABT.ABT_size
ABST_height = ABT.ABT_height
ABST_depth = ABT.ABT_depth

## Tree contents/queries/traversals

ABST_traverse = ABT.ABT_traverse

def ABST_search(tree, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER):
    index = _ABST_search(tree, value, key=key, order=order)
    if index < len(tree) and tree[index] is not None:
        return tree[index][VALUE_KEY]
    return None

def ABST_contains(tree, value, /, *, key=None):
    if ABST_search(tree, value, key=key) is None:
        return False
    return True

def ABST_min(tree, index=0, /):
    index, depth = _ABST_leftmost(tree, index)
    return tree[index][VALUE_KEY]

def ABST_max(tree, index=0, /):
    index, depth = _ABST_rightmost(tree, index)
    return tree[index][VALUE_KEY]
    
# TODO: ABST_rank
    
# TODO: ABST_select(tree, k) # O(N), ABST_selectN(tree, k: Iterable)
                
# CONSIDER: might be able to speed this up to O(k*logn) where k is the number of elements with the same value by utilizing _ABST_search
# WARNING: don't use this directly, subject to change signature; specifically the output
#ABST_find = ABT.ABT_find

# currently O(N)...could be faster
ABST_count = ABT.ABT_count

def ABST_validate(tree, /, *, key=None, unique=False):
    result = [True]
    if key is None:
        def validate_node(tree, index, result):
            # left child
            child = _move(index, DIR_LEFT)
            if tree[child] is not None:
                if unique and tree[child][VALUE_KEY] == tree[index][VALUE_KEY]: # not unique
                    result[0] = False
                    return TRAVERSE_STOP
                elif tree[child][VALUE_KEY] > tree[index][VALUE_KEY]: # not sorted
                    result[0] = False
                    return TRAVERSE_STOP
            # right child
            child = _move(index, DIR_RIGHT)
            if tree[child] is not None:
                if unique and tree[child][VALUE_KEY] == tree[index][VALUE_KEY]: # not unique
                    result[0] = False
                    return TRAVERSE_STOP
                elif tree[child][VALUE_KEY] < tree[index][VALUE_KEY]: # not sorted
                    result[0] = False
                    return TRAVERSE_STOP
            return TRAVERSE_GO
        ABST_traverse(tree, validate_node, result, traversal=TRAVERSE_LEVELORDER)
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
            return TRAVERSE_GO
        ABST_traverse(tree, validate_node, result, key, traversal=TRAVERSE_LEVELORDER)
    return result[0]

# node_factory is only meant for specializations that actually requires nodes. For simple BSTs, do not use node_factory unless you correct the key parameters for the node structure
def ABST_add(tree, value, /, *, key=None, unique=False, update=False, node_factory=None):
    N = len(tree)
    root = 0
    if key is None:
        kvalue = value
        while root < N and tree[root] is not None:
            kroot = tree[root][VALUE_KEY]
            if kvalue < kroot:
                root = _move(root, DIR_LEFT)
            elif kvalue > kroot:
                root = _move(root, DIR_RIGHT)
            elif not unique and not update: # allowed to have duplicates
                #root = _ABST_search_rightmost(tree, root, key=key)
                root = _ABST_search_most(tree, root, DIR_RIGHT, key=key)
                
                root = _move(root, DIR_RIGHT)
                while root < N and tree[root] is not None:
                    root = _move(root, DIR_LEFT)
            else: # kvalue == kroot and unique = True
                if update:
                    tree[root][VALUE_KEY] = value
                return tree
    else:
        kvalue = key(value)
        while root < N and tree[root] is not None:
            kroot = key(tree[root][VALUE_KEY])
            if kvalue < kroot:
                root = _move(root, DIR_LEFT)
            elif kvalue > kroot:
                root = _move(root, DIR_RIGHT)
            elif not unique and not update: # allowed to have duplicates
                #root = _ABST_search_rightmost(tree, root, key=key)
                root = _ABST_search_most(tree, root, DIR_RIGHT, key=key)
                
                root = _move(root, DIR_RIGHT)
                while root < N and tree[root] is not None:
                    root = _move(root, DIR_LEFT)
            else: # kvalue == kroot and unique = True
                if update:
                    tree[root][VALUE_KEY] = value
                return tree
    if root >= N:
        _ABST_extend(tree, root + 1)
    if node_factory is None:
        tree[root] = value
    else:
        tree[root] = node_factory(value)
    return tree
    
# TODO: ABST_update(tree_dest, *other_ABSTs, /, unique=False) # merge trees

def ABST_remove(tree, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER):
    N = len(tree)
    root = _ABST_search(tree, value, key=key, order=order)
    if root >= N or tree[root] is None:
        raise KeyError(f"ABST_remove: key {value} not found in tree")
    
    if not _ABST_is_leaf(tree, root):
        child = _move(root, DIR_RIGHT)
        replacement = None
        
        if child < N and tree[child] is not None:
            replacement, replacement_depth = _ABST_leftmost(tree, child)
            dir_ = DIR_RIGHT
        child = _move(root, DIR_LEFT)
        if child < N and tree[child] is not None:
            leaf, depth = _ABST_rightmost(tree, child)
            if replacement is None or depth > replacement_depth:
                replacement = leaf
                dir_ = DIR_LEFT
                
        _ABST_swap(tree, root, replacement)
        root = replacement
        if not _ABST_is_leaf(tree, root):
            tree[root] = None # have to set to None after since otherwise _ABST_is_leaf will return False
            _ABST_move_subtree(tree, _move(root, dir_), root)
        else:
            tree[root] = None
    else:
        tree[root] = None
    return tree

def ABST_discard(tree, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER, path=None):
    if path is None:
        path = []
    try:
        return ABST_remove(tree, value, key=key, order=order, path=path)
    except KeyError:
        return tree

ABST_equals = ABT.ABT_equals