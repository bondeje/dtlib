# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 10:17:37 2022

@author: jeffr
"""

from collections.abc import Iterable
import dtlib.trees._ArrayBinarySearchTree as ABST
import dtlib.trees._ArrayBinaryTree as ABT
import dtlib.trees._Node as _Node
from dtlib.trees._constants import DIR_PARENT, DIR_LEFT, DIR_RIGHT, \
    VALUE_KEY, TRAVERSE_GO, TRAVERSE_STOP, BT_BALANCED, \
    TRAVERSE_LEVELORDER, DEFAULT_SEARCH_ORDER, LIST_NODE, \
    SEARCH_FIRST_INORDER, SEARCH_LAST_INORDER
    
# TODO: create iterator classes for each type of iteration
# TODO: Iterable = AOST_iter(tree, /, *, traversal='inorder')

############################## Module globals ################################

## utilizing BLib.Trees._constants

SIZE_KEY = 1
DEFAULT_NODE_FACTORY = _Node.Node_factory(LIST_NODE, {SIZE_KEY: 1})

################################ UTILITIES ####################################

## comment out aliasing into namespace until they are actually needed. Left
## here for documentation purposes

#_AOST_is_leaf = ABT._ABT_is_leaf
# faster method since we have access to size
def _AOST_is_leaf(tree, index):
    return _AOST_size(tree, index) == 1

_AOST_move_index = ABT._ABT_move_index
_move = _AOST_move_index

# O(1) instead of O(n)
def _AOST_size(tree, index):
    if tree[index] is None:
        return 0
    return tree[index][SIZE_KEY]

def _AOST_update_size(tree, index):
    tree[index][SIZE_KEY] = 1 + tree[_move(index, DIR_LEFT)][SIZE_KEY] + tree[_move(index, DIR_RIGHT)][SIZE_KEY]

_AOST_diameter = ABT._ABT_diameter

_AOST_depth = ABT._ABT_depth

_AOST_extend = ABT._ABT_extend

_AOST_swap = ABT._ABT_swap

_AOST_move_subtree = ABT._ABT_move_subtree

_AOST_leftmost = ABT._ABT_leftmost

_AOST_rightmost = ABT._ABT_rightmost

_AOST_search_most = ABST._ABST_search_most

_AOST_search = ABST._ABST_search

# fairly certain this is still NlogM where M is the number of elements in the AWBT and N is the number of k values, which probably difficult to show; it is definitely true in the worst case
# this is still going to be faster than N calls to AWBT_select as we do not have to restart at the root for the traversal
def _AOST_select_N(tree, k):
    k = sorted(k)
    M = len(k)
    out = [None]*M
    root = 0
    N = AOST_size(tree, root)
    if k[0] >= N:
        return out
    
    i = 0
    _path = -1
    root_k = [AOST_size(tree, _move(root, DIR_LEFT))]
    while i < M and k[i] < N:
        while root_k[-1] != k[i]:
            _path = root
            if root_k[-1] < k[i]:
                root = _move(root, DIR_RIGHT)
                root_k.append(root_k[-1] + AOST_size(tree, _move(root, DIR_LEFT)) + 1) # add node's left subtree to k as well as parent node
            else:
                root = _move(root, DIR_LEFT)
                root_k.append(root_k[-1] - AOST_size(tree, _move(root, DIR_RIGHT)) - 1) # remove right subtree and node from count
        out[i] = tree[root][VALUE_KEY]
        i += 1
        # reverse up the path until we find a node that would have resulted in a move to the right
        # do not have to protect against _path >= 0 because it is only == -1 if len(root_k) == 1
        while i < M and len(root_k) > 1 and root_k[-2] <= k[i]: # meaning the current node's parent is smaller in k than target...move up to next parent
            root = _path
            _path = _move(_path, DIR_PARENT)
            root_k.pop()
            
    return out

################################# Traversals ##################################

## using the public API from ABT as the implementation is identical

################################# Public API ##################################


def AOST_create(contents=None, Nmin=0, /, *, key=None, inplace=False, binary_tree_type=BT_BALANCED, node_factory=DEFAULT_NODE_FACTORY):
    return ABST.ABST_create(contents, Nmin, key=key, inplace=inplace, binary_tree_type=binary_tree_type, node_factory=node_factory)
    
## Tree properties/geometry

AOST_size = _AOST_size
AOST_height = ABT.ABT_height
AOST_depth = ABT.ABT_depth

## Tree contents/queries/traversals

AOST_traverse = ABT.ABT_traverse

AOST_search = ABST.ABST_search

def AOST_select(tree, k, /):
    if isinstance(k, Iterable):
        return _AOST_select_N(tree, sorted(k))
    N = len(tree)
    if k >= N:
        return None # probably should raise a ValueError instead
    root = 0
    root_k = AOST_size(tree, _move(root, DIR_LEFT))
    while root < N and tree[root] is not None and root_k != k:
        if root_k < k:
            root = _move(root, DIR_RIGHT) # move root right
            root_k += AOST_size(tree, _move(root, DIR_LEFT)) + 1 # add node's left subtree to k as well as parent node
        else:
            root = _move(root, DIR_LEFT)
            root_k -= AOST_size(tree, _move(root, DIR_RIGHT)) + 1 # remove right subtree and node from count
    return tree[root][VALUE_KEY]

def AOST_rank(tree, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER):
    index = _AOST_search(tree, value, key=key, order=order)
    if index >= len(tree):
        return None
    return tree[_move(index, DIR_LEFT)][SIZE_KEY]

AOST_contains = ABST.ABST_contains

AOST_min = ABST.ABST_min

AOST_max = ABST.ABST_max
                
# CONSIDER: might be able to speed this up to O(k*logn) where k is the number of elements with the same value by utilizing _ABST_search
# WARNING: don't use this directly, subject to change signature; specifically the output
#ABST_find = ABT.ABT_find

# currently O(N)...could be faster
#TODO: this is where it can certainly be faster by finding the rank of the last occurrence minus the last occurrence
#AOST_count = ABT.ABT_count
#TODO: really need to test the implementation. This should be O(logN)
def AOST_count(tree, value, /, *, key=None):
    return AOST_rank(tree, value, key=key, order=SEARCH_LAST_INORDER) - AOST_rank(tree, value, key=key, order=SEARCH_FIRST_INORDER) + 1

def AOST_validate(tree, /, *, key=None, unique=False):
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
            return TRAVERSE_GO
        AOST_traverse(tree, validate_node, result, traversal=TRAVERSE_LEVELORDER)
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
            return TRAVERSE_GO
        AOST_traverse(tree, validate_node, result, key, traversal=TRAVERSE_LEVELORDER)
    return result[0]

# path output will NOT include node added
def AOST_add(tree, value, /, *, key=None, unique=False, update=False, node_factory=DEFAULT_NODE_FACTORY, path=None):
    if path is None:
        path = []
    node = node_factory(value)
    root = 0
    N = len(tree)
    if key is None:
        kvalue = value
        while root < N and tree[root] is not None:
            path.append(root)
            kroot = tree[root][VALUE_KEY]
            if kvalue < kroot: # move root left
                root = _move(root, DIR_LEFT)
            elif kvalue > kroot: # move root right
                root = _move(root, DIR_RIGHT)
            elif not unique and not update: # allowed to have duplicates
                path.pop()
                root = _AOST_search_most(tree, root, DIR_RIGHT, key=key, path=path)
                root = _move(root, DIR_RIGHT)
                if root < N and tree[root] is not None:
                    root, depth = _AOST_leftmost(tree, root, path=path)
                    root = _move(root, DIR_LEFT)
            else: # the key is already found and unique is True; exit without making changes to tree.
                #if udpate: # this really does nothing when key == None, but is needed if key != None
                #    tree[root][VALUE_KEY] = value
                return tree# do nothing
    else:
        kvalue = key(value)
        while root < N and tree[root] is not None:
            path.append(root)
            kroot = key(tree[root][VALUE_KEY])
            if kvalue < kroot: # move root left
                root = _move(root, DIR_LEFT)
            elif kvalue > kroot: # move root right
                root = _move(root, DIR_RIGHT)
            elif not unique and not update: # allowed to have duplicates
                path.pop()
                root = _AOST_search_most(tree, root, DIR_RIGHT, key=key, path=path)
                root = _move(root, DIR_RIGHT)
                if root < N and tree[root] is not None:
                    root, depth = _AOST_leftmost(tree, root, path=path)
                    root = _move(root, DIR_LEFT)
            else: # the key is already found and unique is True; exit without making changes to tree.
                if update: # this really does nothing when key == None, but is needed if key != None
                    tree[root][VALUE_KEY] = value
                return tree# do nothing
    
    # at this point, root should be >= N or tree[root] and last element in _path is the parent
    # that is supposed to receive the new node on the child to _dir direction
    
    # make sure tree is long enough
    if root >= N:
        _AOST_extend(tree, root+1)
    
    # insert the new node
    tree[root] = node
    for p in path:
        tree[p][SIZE_KEY] += 1
    return tree
    
# TODO: ABST_update(tree_dest, *other_ABSTs, /, unique=False) # merge trees

# path output will NOT include node removed
def AOST_remove(tree, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER, path=None):
    if path is None:
        path = []
    N = len(tree)
    if not N:
        return ValueError(f"Empty WeightBalancedTree does not contain {value}")
    root = _AOST_search(tree, value, key=key, order=order, path=path)
    # need to run through path and reduce size by 1 if element is actually removed
    
    if root >= N or tree[root] is None: # value not found
        raise KeyError(f"ABST_remove: key {value} not found in tree")
    
    node_to_remove = tree[root]
    if key is None:
        assert node_to_remove[VALUE_KEY] == value
    else:
        assert key(node_to_remove[VALUE_KEY]) == value
    
    # if node to remove has children, need to replace the value, 
    if AOST_size(tree, root) > 1: # node is not a leaf, need to move up a descendent
        #path_remove_index = len(_path) # reference to where the node in _path is that needs to change    
    
        # traverse a different path depending on which subtree is larger.
        # at the end, root holds the node to replace
        if AOST_size(tree, _move(root, DIR_LEFT)) > AOST_size(tree, _move(root, DIR_RIGHT)): # left subtree is nonempty and bigger than right subtree so pull up postorder predecessor
            root, depth = _AOST_rightmost(tree, _move(root, DIR_LEFT), path=path)
            replacement_node = tree[root]
            tree[root] = None
            _AOST_move_subtree(tree, _move(root, DIR_LEFT), root)
        else: # right subtree is nonempty and at least as big as left subtree so pull up preorder postdecessor
            root, depth = _AOST_leftmost(tree, _move(root, DIR_RIGHT), path=path)
            replacement_node = tree[root]
            tree[root] = None
            _AOST_move_subtree(tree, _move(root, DIR_RIGHT), root)
        # swap the value in root to node_to_remove; no need to move children
        node_to_remove[VALUE_KEY], replacement_node[VALUE_KEY] = replacement_node[VALUE_KEY], node_to_remove[VALUE_KEY]
    else: # node_to_remove is a leaf, just remove it from the parent
        tree[root] = None
    path.pop() # top before this is the "root" index that will be removed/set to null and all replacements and subtrees are unaffected by size changes
    for p in path:
        tree[p][SIZE_KEY] -= 1
    return tree

#TODO need extensive modification...pull from ArrayWeightBalancedTree without _rebalance call
def AOST_discard(tree, value, /, *, key=None, order=DEFAULT_SEARCH_ORDER, path=None):
    if path is None:
        path = []
    try:
        return AOST_remove(tree, value, key=key, order=order, path=path)
    except KeyError:
        return tree

