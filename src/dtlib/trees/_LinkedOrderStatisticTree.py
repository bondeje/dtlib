# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 23:31:58 2022

@author: jeffr
"""

from collections.abc import Iterable
import dtlib.trees._LinkedBinarySearchTree as LBST
import dtlib.trees._LinkedBinaryTree as LBT
import dtlib.trees._Node as _Node
from dtlib.trees._constants import DIR_LEFT, DIR_RIGHT, \
    VALUE_KEY, TRAVERSE_GO, TRAVERSE_STOP, BT_BALANCED, \
    TRAVERSE_LEVELORDER, DEFAULT_SEARCH_ORDER, LIST_NODE, \
    SEARCH_FIRST_INORDER, SEARCH_LAST_INORDER
    
# TODO: create iterator classes for each type of iteration
# TODO: Iterable = LOST_iter(tree, /, *, traversal='inorder')

############################## Module globals ################################

## utilizing BLib.Trees._constants

SIZE_KEY = 3
DEFAULT_NODE_FACTORY = _Node.Node_factory(LIST_NODE, {DIR_LEFT: None, DIR_RIGHT: None, SIZE_KEY: 1})

################################ UTILITIES ####################################

## comment out aliasing into namespace until they are actually needed. Left
## here for documentation purposes

#_LOST_is_leaf = ABT._ABT_is_leaf
# faster method since we have access to size
def _LOST_is_leaf(node):
    return _LOST_size(node) == 1

# O(1) instead of O(n)
def _LOST_size(node):
    if node is None:
        return 0
    return node[SIZE_KEY]

def _LOST_update_size(root, node=None):
    if node is not None:
        root = node
    if root is not None:
        root[SIZE_KEY] = 1 + root[DIR_LEFT][SIZE_KEY] + root[DIR_RIGHT][SIZE_KEY]

_LOST_diameter = LBT._LBT_diameter

_LOST_depth = LBT._LBT_depth

_LOST_swap = LBT._LBT_swap

_LOST_leftmost = LBT._LBT_leftmost

_LOST_rightmost = LBT._LBT_rightmost

_LOST_search_most = LBST._LBST_search_most

_LOST_search = LBST._LBST_search

# fairly certain this is still NlogM where M is the number of elements in the LWBT and N is the number of k values, which probably difficult to show; it is definitely true in the worst case
# this is still going to be faster than N calls to LWBT_select as we do not have to restart at the root for the traversal
def _LOST_select_N(root, k):
    k = sorted(k)
    M = len(k)
    out = [None]*M
    if root is None:
        return out
    N = root[SIZE_KEY]
    i = 0
    _path = []
    root_k = [LOST_size(root[DIR_LEFT])]
    while i < M and k[i] < N:
        while root_k[-1] != k[i]:
            _path.append(root)
            if root_k[-1] < k[i]:
                root = root[DIR_RIGHT]
                root_k.append(root_k[-1] + LOST_size(root[DIR_LEFT]) + 1) # add node's left subtree to k as well as parent node
            else:
                root = root[DIR_LEFT]
                root_k.append(root_k[-1] - LOST_size(root[DIR_RIGHT]) - 1) # remove right subtree and node from count
        out[i] = root[VALUE_KEY]
        i += 1
        # reverse up the path until we find a node that would have resulted in a move to the right
        while i < M and len(root_k) > 1 and root_k[-2] <= k[i]: # meaning the current node's parent is smaller in k than target
            root = _path.pop()
            root_k.pop()
    
    return out

################################# Traversals ##################################

## using the public API from ABT as the implementation is identical

################################# Public API ##################################


def LOST_create(contents=None, /, *, key=None, binary_tree_type=BT_BALANCED, node_factory=DEFAULT_NODE_FACTORY):
    return LBST.LBST_create(contents, key=key, binary_tree_type=binary_tree_type, node_factory=node_factory)
    
## Tree properties/geometry

LOST_size = _LOST_size
LOST_height = LBT.LBT_height
LOST_depth = LBT.LBT_depth

## Tree contents/queries/traversals

LOST_traverse = LBT.LBT_traverse

LOST_search = LBST.LBST_search

def LOST_select(root, k):
    if isinstance(k, Iterable):
        return _LOST_select_N(root, sorted(k))
    if root is None:
        return None # probably should raise a ValueError instead
    root_k = LOST_size(root[DIR_LEFT])
    while root and root_k != k:
        if root_k < k:
            root = root[DIR_RIGHT] # move root right
            root_k += LOST_size(root[DIR_LEFT]) + 1 # add node's left subtree to k as well as parent node
        else:
            root = root[DIR_LEFT]
            root_k -= LOST_size(root[DIR_RIGHT]) + 1 # remove right subtree and node from count
    return root[VALUE_KEY]

def LOST_rank(root, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER):
    node = _LOST_search(root, value, key=key, order=order)
    if node is None:
        return node
    return node[DIR_LEFT][SIZE_KEY]

LOST_contains = LBST.LBST_contains

LOST_min = LBST.LBST_min

LOST_max = LBST.LBST_max
                
# CONSIDER: might be able to speed this up to O(k*logn) where k is the number of elements with the same value by utilizing _ABST_search
# WARNING: don't use this directly, subject to change signature; specifically the output
#ABST_find = ABT.ABT_find

# currently O(N)...could be faster
#TODO: this is where it can certainly be faster by finding the rank of the last occurrence minus the last occurrence
#LOST_count = LBT.LBT_count
#TODO: really need to test the implementation. This should be O(logN)
def LOST_count(tree, value, /, *, key=None):
    return LOST_rank(tree, value, key=key, order=SEARCH_LAST_INORDER) - LOST_rank(tree, value, key=key, order=SEARCH_FIRST_INORDER) + 1

def LOST_validate(root, /, *, key=None, unique=False):
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
            return TRAVERSE_GO
        LOST_traverse(root, validate_node, result, traversal=TRAVERSE_LEVELORDER)
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
            return TRAVERSE_GO
        LOST_traverse(root, validate_node, result, key, traversal=TRAVERSE_LEVELORDER)
    return result[0]

#TODO: I am here in updating

# path output will NOT include node added
def LOST_add(root, value, /, *, key=None, unique=False, update=False, node_factory=DEFAULT_NODE_FACTORY, path=None):
    if path is None:
        path = []
    nvalue = node_factory(value)
    if root is None:
        return nvalue
    node = root
    dir_ = DIR_RIGHT
    if key is None:
        kvalue = value
        while node is not None:
            path.append(node)
            kroot = node[VALUE_KEY]
            if kvalue < kroot: # move node left
                dir_ = DIR_LEFT
                node = node[dir_]
            elif kvalue > kroot: # move node right
                dir_ = DIR_RIGHT
                node = node[dir_]
            elif not unique and not update: # allowed to have duplicates
                path.pop()
                node = _LOST_search_most(root, node, DIR_RIGHT, key=key, path=path)
                dir_ = DIR_RIGHT
                node = node[dir_]
                if node is not None:
                    node, depth = _LOST_leftmost(root, node, path=path)
                    dir_ = DIR_LEFT
                    node = node[dir_]
            else: # the key is already found and unique is True; exit without making changes to tree.
                #if udpate: # this really does nothing when key == None, but is needed if key != None
                #    tree[root][VALUE_KEY] = value
                return root# do nothing
    else:
        kvalue = key(value)
        while node is not None:
            path.append(node)
            kroot = key(node[VALUE_KEY])
            if kvalue < kroot: # move node left
                dir_ = DIR_LEFT
                node = node[dir_]
            elif kvalue > kroot: # move node right
                dir_ = DIR_RIGHT
                node = node[dir_]
            elif not unique and not update: # allowed to have duplicates
                path.pop()
                node = _LOST_search_most(root, node, DIR_RIGHT, key=key, path=path)
                dir_ = DIR_RIGHT
                node = node[dir_]
                if node is not None:
                    node, depth = _LOST_leftmost(root, node, path=path)
                    dir_ = DIR_LEFT
                    node = node[dir_]
            else: # the key is already found and unique is True; exit without making changes to tree.
                if update: # this really does nothing when key == None, but is needed if key != None
                    node[VALUE_KEY] = value
                return root# do nothing
    
    # at this point, node should be None and last element in _path is the parent
    # that is supposed to receive the new node on the child to _dir direction
    
    # insert the new node
    path[-1][dir_] = nvalue
    for p in path:
        p[SIZE_KEY] += 1
    return root
    
# TODO: ABST_update(tree_dest, *other_ABSTs, /, unique=False) # merge trees

# path output will NOT include node removed
def LOST_remove(root, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER, path=None):
    if path is None:
        path = []
    if root is None:
        return ValueError(f"Empty WeightBalancedTree does not contain {value}")
    node = _LOST_search(root, value, key=key, order=order, path=path)
    # need to run through path and reduce size by 1 if element is actually removed
    
    if node is None: # value not found
        raise KeyError(f"ABST_remove: key {value} not found in tree")
    
    node_to_remove = node
    if key is None:
        assert node_to_remove[VALUE_KEY] == value
    else:
        assert key(node_to_remove[VALUE_KEY]) == value
    
    # if node to remove has children, need to replace the value, 
    if LOST_size(node) > 1: # node is not a leaf, need to move up a descendent
        #path_remove_index = len(_path) # reference to where the node in _path is that needs to change    
    
        # traverse a different path depending on which subtree is larger.
        # at the end, root holds the node to replace
        if LOST_size(node[DIR_LEFT]) > LOST_size(node[DIR_RIGHT]): # left subtree is nonempty and bigger than right subtree so pull up postorder predecessor
            node, depth = _LOST_rightmost(root, node[DIR_LEFT], path=path)

            replacement_node = path.pop()
            if path[-1] is node_to_remove: # replacement path's parent is the node to remove; skip over replacement nodes
                node_to_remove[DIR_LEFT] = replacement_node[DIR_LEFT]
            else: # rightmost node has parent as path[-1] whose right child must be replaced with replacement node's left child
                path[-1][DIR_RIGHT] = replacement_node[DIR_LEFT]
        else: # right subtree is nonempty and at least as big as left subtree so pull up preorder postdecessor
            node, depth = _LOST_leftmost(root, node[DIR_RIGHT], path=path)
            replacement_node = path.pop()
            if path[-1] is node_to_remove: # replacement path's parent is the node to remove; skip over replacement nodes
                node_to_remove[DIR_RIGHT] = replacement_node[DIR_RIGHT]
            else: # leftmost node has parent as path[-1] whose left child must be replaced with replacement node's right child
                path[-1][DIR_LEFT] = replacement_node[DIR_RIGHT]
        # swap the value in root to node_to_remove; no need to move children
        node_to_remove[VALUE_KEY] = replacement_node[VALUE_KEY]
        replacement_node = None
    else: # node_to_remove is a leaf, just remove it from the parent
        path.pop()
        if path:
            if path[-1][DIR_RIGHT] == node_to_remove:
                path[-1][DIR_RIGHT] = None
            else:
                path[-1][DIR_LEFT] = None
            node_to_remove = None
        else:
            node_to_remove = None
            return None
    
    for p in path:
        p[SIZE_KEY] -= 1
    return root

#TODO need extensive modification...pull from ArrayWeightBalancedTree without _rebalance call
def LOST_discard(root, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER, path=None):
    if path is None:
        path = []
    try:
        return LOST_remove(root, value, key=key, order=order, path=path)
    except KeyError:
        return root

