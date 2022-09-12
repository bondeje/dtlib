# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 13:21:43 2022

@author: jeffr
"""

from collections.abc import Iterable
import dtlib.trees._LinkedBinaryTree as LBT
import dtlib.trees._Node as _Node
from dtlib.trees._constants import DIR_LEFT, DIR_RIGHT, \
    DIR_PARENT, VALUE_KEY, TRAVERSE_GO, TRAVERSE_STOP, \
    TRAVERSE_LEVELORDER, SEARCH_FIRST_INORDER, \
    SEARCH_LAST_INORDER, DEFAULT_SEARCH_ORDER, BT_BALANCED, \
    BT_COMPLETE, LIST_NODE
from operator import lt, gt

# TODO: create iterator classes for each type of iteration
# TODO: Iterable = ABST_iter(tree, /, *, traversal='inorder')

############################## Module globals ################################

## utilizing BLib.Trees._constants

DEFAULT_NODE_FACTORY = _Node.Node_factory(LIST_NODE, {DIR_LEFT: None, DIR_RIGHT: None})

################################ UTILITIES ####################################

## comment out aliasing into namespace until they are actually needed. Left
## here for documentation purposes

_LBST_is_leaf = LBT._LBT_is_leaf

_LBST_size = LBT.LBT_size

_LBST_diameter = LBT._LBT_diameter

_LBST_depth = LBT._LBT_depth

_LBST_swap = LBT._LBT_swap

_LBST_leftmost = LBT._LBT_leftmost

_LBST_rightmost = LBT._LBT_rightmost

# specicalization of _LBST_search. key(tree[index]) == key(value) or tree[index] == value must be satisfied
def _LBST_search_most(root, node=None, dir_=None, /, *, key=None, path=None):
    if path is None:
        path = []
    if node is not None:
        root = node
    if dir_ == DIR_LEFT:
        _leader, _follower, cmp = DIR_LEFT, DIR_RIGHT, lt
    else:
        _leader, _follower, cmp = DIR_RIGHT, DIR_LEFT, gt
    #most = root
    if key is None:
        value = root[VALUE_KEY]
        while root is not None:
            kroot = root[VALUE_KEY]
            if kroot == value:
                #most = root
                path.append(root)
                root = root[_leader]
            elif cmp(kroot, value): # was kroot < value for _LBST_search_leftmost
                path.append(root)
                root = root[_follower]
            else:
                root = None # exit condition
                #return most
        while path[-1][VALUE_KEY] != value:
            path.pop()
    else:
        value = key(root[VALUE_KEY])
        while root is not None:
            kroot = key(root[VALUE_KEY])
            if kroot == value:
                #most = root
                path.append(root)
                root = root[_leader]
            elif cmp(kroot, value): # was kroot < value for _LBST_search_leftmost
                path.append(root)
                root = root[_follower]
            else:
                root = None # exit condition
                #return most
        while key(path[-1][VALUE_KEY]) != value:
            path.pop()
    #return most
    return path[-1]

# TODO: find a way to inject uniqueness into the search; otherwise the leftmost and rightmost are triggered and full O(height) is computed
def _LBST_search(root, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER, path=None):
    if path is None:
        path = []
    if key is None:
        while root is not None:
            path.append(root)
            kroot = root[VALUE_KEY]
            if kroot == value:
                break # continue with root
            elif kroot < value:
                root = root[DIR_RIGHT]
            else:
                root = root[DIR_LEFT]
    else:
        while root is not None:
            path.append(root)
            kroot = key(root[VALUE_KEY])
            if kroot == value:
                break # continue with root
            elif kroot < value:
                root = root[DIR_RIGHT]
            else:
                root = root[DIR_LEFT]
    
    if root is not None:
        if order == SEARCH_FIRST_INORDER:
            path.pop()
            root = _LBST_search_most(root, None, DIR_LEFT, key=key, path=path)
        elif order == SEARCH_LAST_INORDER:
            path.pop()
            root = _LBST_search_most(root, None, DIR_RIGHT, key=key, path=path)
        else:
            pass
    return root

################################# Traversals ##################################

## using the public API from ABT as the implementation is identical

################################# Public API ##################################

def LBST_create(contents, /, *, key=None, binary_tree_type=BT_BALANCED, node_factory=DEFAULT_NODE_FACTORY):
    if isinstance(contents, Iterable):
        contents = sorted(contents, key=key)
    else:
        contents = [contents]
        
    return LBT.LBT_create(contents, binary_tree_type=binary_tree_type, node_factory=node_factory)

## Tree properties/geometry

LBST_size = _LBST_size
LBST_height = LBT.LBT_height
LBST_depth = _LBST_depth

## Tree contents/queries/traversals

LBST_traverse = LBT.LBT_traverse

def LBST_search(root, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER):
    node = _LBST_search(root, value, key=key, order=order)
    if node is None:
        return node[VALUE_KEY]
    return None

def LBST_contains(root, value, /, *, key=None):
    if LBST_search(root, value, key=key) is None:
        return False
    return True

def LBST_min(root, node=None, /):
    node, depth = _LBST_leftmost(root, node)
    return node[VALUE_KEY]

def LBST_max(root, node=None, /):
    node, depth = _LBST_rightmost(root, node)
    return node[VALUE_KEY]

# TODO: ABST_rank
    
# TODO: ABST_select(tree, k) # O(N), ABST_selectN(tree, k: Iterable)
                
# CONSIDER: might be able to speed this up to O(k*logn) where k is the number of elements with the same value by utilizing _ABST_search
# WARNING: don't use this directly, subject to change signature; specifically the output
#LBST_find = LBT.LBT_find

# currently O(N)...could be faster
LBST_count = LBT.LBT_count

def LBST_validate(root, /, *, key=None, unique=False):
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
            # right child
            child = node[DIR_RIGHT]
            if child is not None:
                if unique and child[VALUE_KEY] == node[VALUE_KEY]: # not unique
                    result[0] = False
                    return TRAVERSE_STOP
                elif child[VALUE_KEY] < node[VALUE_KEY]: # not sorted
                    result[0] = False
                    return TRAVERSE_STOP
            return TRAVERSE_GO
        LBST_traverse(root, validate_node, result, traversal=TRAVERSE_LEVELORDER)
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
            return TRAVERSE_GO
        LBST_traverse(root, validate_node, result, key, traversal=TRAVERSE_LEVELORDER)
    return result[0]

def LBST_add(root, value, /, *, key=None, unique=False, update=False, node_factory=DEFAULT_NODE_FACTORY):
    if root is None:
        return node_factory(value)
    node = root
    parent = None
    if key is None:
        kvalue = value
        while node is not None:
            knode = node[VALUE_KEY]
            if kvalue < knode:
                parent = node
                dir_ = DIR_LEFT
                node = parent[dir_]
            elif kvalue > knode:
                parent = node
                dir_ = DIR_RIGHT
                node = parent[dir_]
            elif not unique and not update: # allowed to have duplicates
                parent = _LBST_search_most(root, node, DIR_RIGHT, key=key)
                dir_ = DIR_RIGHT
                node = parent[dir_]
                if node is not None:
                    dir_ = DIR_LEFT
                    while node is not None:
                        parent = node
                        node = parent[dir_]
            else: # kvalue == kroot and unique = True
                if update:
                    node[VALUE_KEY] = value
                return root
    else:
        kvalue = key(value)
        while node is not None:
            knode = key(node[VALUE_KEY])
            if kvalue < knode:
                #print(f"moving left for {kvalue} < {knode}")
                parent = node
                dir_ = DIR_LEFT
                node = parent[dir_]
            elif kvalue > knode:
                #print(f"moving right for {kvalue} < {knode}")
                parent = node
                dir_ = DIR_RIGHT
                node = parent[dir_]
            elif not unique and not update: # allowed to have duplicates
                #print(f"not unique and not update...finding repeats for {kvalue} == {knode}")
                parent = _LBST_search_most(root, node, DIR_RIGHT, key=key)
                dir_ = DIR_RIGHT
                node = parent[dir_]
                if node is not None:
                    dir_ = DIR_LEFT
                    while node is not None:
                        parent = node
                        node = parent[dir_]
            else: # kvalue == kroot and unique = True
                #print(f"unique, possibly updating {kvalue} == {knode}")
                if update:
                    node[VALUE_KEY] = value
                return root
    parent[dir_] = node_factory(value)
    
    return root

# TODO: LBST_update(tree_dest, *other_LBSTs, /, unique=False) # merge trees

def LBST_remove(root, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER):
    path = []
    node = _LBST_search(root, value, key=key, path=path, order=order)
    #print(node)
    if len(path) > 1:
        node_p = path[-2]
        #parent = path[-2]
    else:
        node_p = None
        #parent = None
    if node is None:
        raise KeyError(f"LBST_remove: key {value} not found in tree")
        
    if _LBST_is_leaf(node):
        if node_p is not None:
            if node_p[DIR_RIGHT] == node:
                node_p[DIR_RIGHT] = None
            else:
                node_p[DIR_LEFT] = None
        else:
            root = None
    elif node[DIR_RIGHT] is None: # node[DIR_LEFT] is not None
        if node_p is None:
            root = node[DIR_LEFT]
        else:
            if node_p[DIR_LEFT] == node:
                node_p[DIR_LEFT] = node[DIR_LEFT]
            else:
                node_p[DIR_RIGHT] = node[DIR_LEFT]
        node[DIR_LEFT] = None
    elif node[DIR_LEFT] is None: # node[DIR_RIGHT] is not None
        if node_p is None:
            root = node[DIR_RIGHT]
        else:
            if node_p[DIR_LEFT] == node:
                node_p[DIR_LEFT] = node[DIR_RIGHT]
            else:
                node_p[DIR_RIGHT] = node[DIR_RIGHT]
        node[DIR_RIGHT] = None
    else:
        rchild = node[DIR_RIGHT]
        rreppath = []
        rrep, rrep_depth = _LBST_leftmost(rchild, path=rreppath)
        lchild = node[DIR_LEFT]
        lreppath = []
        lrep, lrep_depth = _LBST_rightmost(lchild, path=lreppath)
        
        if rrep_depth >= lrep_depth: # replace with element from right subtree
            if len(rreppath) == 1: # rrep is rchild; just remove node
                rrep[DIR_LEFT] = lchild
                node[DIR_LEFT] = None
                node[DIR_RIGHT] = None
                if node_p is None: # node is root
                    root = rrep
                else:
                    if node_p[DIR_RIGHT] == node:
                        node_p[DIR_RIGHT] = rrep
                    else:
                        node_p[DIR_LEFT] = rrep
            else: # rreppath[-2] is rrep's parent
                _LBST_swap(node, rrep) # swap values...
                node = rrep # node is now in rrep's original position
                rreppath[-2][DIR_LEFT] = node[DIR_RIGHT]
                node[DIR_RIGHT] = None
        else: # replace with element from left subtree
            if len(lreppath) == 1: # lrep is lchild; just remove node
                lrep[DIR_RIGHT] = rchild
                node[DIR_LEFT] = None
                node[DIR_RIGHT] = None
                if node_p is None: # node is root
                    root = lrep
                else:
                    if node_p[DIR_RIGHT] == node:
                        node_p[DIR_RIGHT] = lrep
                    else:
                        node_p[DIR_LEFT] = lrep
            else: # lreppath[-2] is lrep's parent
                _LBST_swap(node, lrep) # swap values...
                node = lrep # node is now in lrep's original position
                lreppath[-2][DIR_RIGHT] = node[DIR_LEFT]
                node[DIR_LEFT] = None
    
    """
    if _LBST_is_leaf(node):
        if parent is not None:
            if parent[DIR_RIGHT] == node:
                parent[DIR_RIGHT] = None
            else:
                parent[DIR_LEFT] = None
    elif node[DIR_RIGHT] is None: # node[DIR_LEFT] is not None
        if parent is None:
            root = node[DIR_LEFT]
        else:
            if parent[DIR_LEFT] == node:
                parent[DIR_LEFT] = node[DIR_LEFT]
            else:
                parent[DIR_RIGHT] = node[DIR_LEFT]
        node[DIR_LEFT] = None
    elif node[DIR_LEFT] is None: # node[DIR_RIGHT] is not None
        if parent is None:
            root = node[DIR_RIGHT]
        else:
            if parent[DIR_LEFT] == node:
                parent[DIR_LEFT] = node[DIR_RIGHT]
            else:
                parent[DIR_RIGHT] = node[DIR_RIGHT]
        node[DIR_RIGHT] = None
    else: # node[DIR_RIGHT] and node[DIR_LEFT] are both not None
        child = node[DIR_RIGHT]
        path.clear()
        path.append(parent)
        path.append(node)
        replacement, replacement_depth = _LBST_leftmost(child, path=path)
        parent = path[-2]
        #print("leftmost of right child", replacement, replacement_depth)
                
        child = node[DIR_LEFT]
        path.clear()
        path.append(parent)
        path.append(node)
        leaf, depth = _LBST_rightmost(child, path=path)
        #print("rightmost of left child", leaf, depth)
        if depth > replacement_depth:
            replacement = leaf
            parent = path[-2]
            #print("taking rightmost of left child", replacement)
        #else:
            #print("taking leftmost of right child", replacement)
            
        if parent == node
        
        _LBST_swap(node, replacement)
        node = replacement
        # TODO: need to clean up this next bit of removing references to node
        if not _LBST_is_leaf(node):
            if parent[DIR_LEFT] == node:
                parent[DIR_LEFT] = node[DIR_RIGHT]
                node[DIR_RIGHT] = None
            else:
                parent[DIR_RIGHT] = node[DIR_LEFT]
                node[DIR_LEFT] = None
        else:
            if parent[DIR_LEFT] == node:
                parent[DIR_LEFT] = None
            else:
                parent[DIR_RIGHT] = None

        # destroy node
        """
    return root

def LBST_discard(root, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER):
    try:
        return LBST_remove(root, value, key=key, order=order)
    except KeyError:
        return root
    
LBST_equals = LBT.LBT_equals