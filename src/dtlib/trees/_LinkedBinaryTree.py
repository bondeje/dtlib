# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 21:30:30 2022

@author: jeffr
"""

#import BLib
from collections import deque # for traversals
from collections.abc import Iterable
from dtlib.utils import _interval_root
from dtlib.trees._constants import DIR_LEFT, DIR_RIGHT, \
    DIR_PARENT, VALUE_KEY, BT_BALANCED, BT_COMPLETE, \
    TRAVERSE_GO, TRAVERSE_STOP, TRAVERSE_INORDER, TRAVERSE_PREORDER, \
    TRAVERSE_POSTORDER, TRAVERSE_LEVELORDER, LIST_NODE
#from BLib.Trees import BinaryTree as BT
#import BLib.Trees.BinaryTree as BT
import dtlib.trees._Node as _Node
import turtle # to be removed

# TODO: all the classes
# TODO: create iterator classes for each type of iteration
# TODO: Iterable = ABT_iter(tree, /, *, traversal='inorder')

############################## Module globals ################################

## most taken from dtlib.trees._constants

DEFAULT_NODE_FACTORY = _Node.Node_factory(LIST_NODE, {DIR_LEFT: None, DIR_RIGHT: None})

############################ Module Initialization ############################



################################ UTILITIES ####################################

## Node properties

def _LBT_is_leaf(root, node=None, /):
    if node is not None:
        root = node
    return root[DIR_LEFT] is None and root[DIR_RIGHT] is None

## Tree creation

# sequence_ is mutated!
def _LBT_create_from_sequence(sequence_, *, binary_tree_type=BT_BALANCED, node_factory=_Node.Node_factory(LIST_NODE)): # key is not needed here since not sorting or using the value at all
    _inorder_to_level_order(sequence_, inplace=True, binary_tree_type=BT_BALANCED)
    sequence_[0] = node_factory(sequence_[0])
    parent = -1
    for i in range(1, len(sequence_)):
        if sequence_[i] is not None:
            sequence_[i] = node_factory(sequence_[i])
            # do not have to check if parent is None because BT_BALANCED and BT_COMPLETE binary trees in array form will always have non-None parents
            if i & 1:
                parent += 1
                sequence_[parent][DIR_LEFT] = sequence_[i]
            else:
                sequence_[parent][DIR_RIGHT] = sequence_[i]
            
    return sequence_[0]

## Navigation

def _LBT_move_index(index, dir_, /):
    if dir_ == DIR_PARENT:
        return ((index-1) >> 1)
    #return (index << 1) + 1 + dir_ # depends on DIR_LEFT = 0
    return (index << 1) + (1 if dir_==DIR_LEFT else 2)

_move = _LBT_move_index

## Tree properties/geometry

# size_t = _LBT_size(root, node=None, /) # if node is not None, root is set to the node
def _LBT_size(root, node=None, /):
    if node is not None:
        root = node
    if root is None:
        return 0
    return 1 + _LBT_size(root[DIR_LEFT]) + _LBT_size(root[DIR_RIGHT])

def _LBT_diameter_helper(node, /):
    if node is None:
        return 0, 0
    l_max_diameter, l_height = _LBT_diameter_helper(node[DIR_LEFT])
    r_max_diameter, r_height  = _LBT_diameter_helper(node[DIR_RIGHT])
    return max(l_max_diameter, r_max_diameter, 1 + l_height + r_height), 1 + max(l_height, r_height)

# size_t = _LBT_diameter(root, node=None, /)
def _LBT_diameter(root, node=None, /):
    if node is not None:
        root = node
    if root is None:
        return 0
    return _LBT_diameter_helper(root)[0]

# O(n)
# size_t = _LBT_depth(root, node, /) # repeated appropriate calls to _LBT_height
def _LBT_depth(root, node=None, /):
    if root is None:
        return 0
    if node is None:
        return 1
    return 1 + _LBT_height(root) - _LBT_height(node)


# size_t = _LBT_height(root, node=None, /) # if node is not None, root is set to node
def _LBT_height(root, node=None, /):
    if node is not None:
        root = node
    if root is None:
        return 0
    return 1 + max(_LBT_height(root[DIR_LEFT]), _LBT_height(root[DIR_RIGHT]))

## Tree manipulation

def _LBT_swap(node1, node2):
    node1[VALUE_KEY], node2[VALUE_KEY] = node2[VALUE_KEY], node1[VALUE_KEY]

# root = _LBT_rotate(root, node, dir_, /) # for double rotations, use it repeatedly, root is unused
def _LBT_rotate(root, node, dir_, /): # root is unused
    if node is None:
        return None
    
    if dir_ == DIR_LEFT:
        child = node[DIR_RIGHT]
        if child is None: # cannot rotate node left because right child is None
            return node
        grandchild = child[DIR_LEFT]
        child[DIR_LEFT] = node
        node[DIR_RIGHT] = grandchild # this line really only make sense for BinarySearchTrees
    elif dir_ == DIR_RIGHT:
        child = node[DIR_LEFT]
        if child is None:
            return node
        grandchild = child[DIR_RIGHT]
        child[DIR_RIGHT] = node
        node[DIR_LEFT] = grandchild # this line really only make sense for BinarySearchTrees
    return child

# TODO: _LBT_split_rotate to replace double rotations; this should be more efficient although not as much of a difference for Linked structures as opposed to Array structures

## Internal queries

#TODO: change this do directionless name and add a parameter
# node, size_t = _LBT_rightmost(tree, index=0, /)
def _LBT_leftmost(root, node=None, /, *, path=None):
    if path is None:
        path = []
    if node is not None:
        root = node
    if root is None:
        return None, 0
    while root is not None:
        path.append(root)
        root = root[DIR_LEFT]
    return path[-1], len(path)-1

# index, size_t = _LBT_rightmost(tree, index=0, /)
def _LBT_rightmost(root, node=None, /, *, path=None):
    if path is None:
        path = []
    if node is not None:
        root = node
    if root is None:
        return None, 0
    print(root[VALUE_KEY])
    while root is not None:
        path.append(root)
        root = root[DIR_RIGHT]
    return path[-1], len(path)-1

# [stack of nodes from leaf to root] = _LBT_path_shortest_to_leaves(root, node=None, /)
# not sure this is useful
def _LBT_extremal_paths_to_leaves(root, node=None, /):
    if node is not None:
        root = node
    
    if root is None:
        return [], []
    
    left_max, left_min = _LBT_extremal_paths_to_leaves(root[DIR_LEFT])
    right_max, right_min = _LBT_extremal_paths_to_leaves(root[DIR_RIGHT])
    if not left_max and not right_max: # root is a leaf
        return [root], [root]
    elif not right_max: # left is not empty
        left_max.append(root)
        left_min.append(root)
        return left_max, left_min
    elif not left_max: # right is not empty
        right_max.append(root)
        right_min.append(root)
        return right_max, right_min
    
    left_max.append(root)
    left_min.append(root)
    right_max.append(root)
    right_min.append(root)
    return left_max if len(left_max) > len(right_max) else right_max, left_min if len(left_min) <= len(right_min) else right_min

# [path of nodes] = _LBT_path_to(root, value, /, *, key=None)
# path is from root to node with value
# WARNING: depends on stack ordering in postorder traversal iterative
def _LBT_path_to(root, value, /, *, key=None):
    st_out = []
    if key is None:
        def _LBT_path_to_helper(st, node, value, st_out):
            if node[VALUE_KEY] == value:
                st_out.extend(st)
                st_out.append(node)
                return TRAVERSE_STOP
            return TRAVERSE_GO
        LBT_traverse(root, _LBT_path_to_helper, value, st_out, traversal=TRAVERSE_POSTORDER)
    else:
        def _LBT_path_to_helper(st, node, value, st_out, key):
            if key(node[VALUE_KEY]) == value:
                st_out.extend(st)
                st_out.append(node)
                return TRAVERSE_STOP
            return TRAVERSE_GO
        LBT_traverse(root, _LBT_path_to_helper, value, st_out, key, traversal=TRAVERSE_POSTORDER)
    # fix the stack, which has nodes on the path: specifically the right children that have not been visited of each subtree root
    if not st_out: # value not found
        return st_out
    path = [st_out.pop()]
    while st_out:
        # top of stack's child is top of path. For left children this should always be true, for right children it is after they have been visited but not traversed
        if (st_out[-1][DIR_RIGHT] is path[-1]) or (st_out[-1][DIR_LEFT] is path[-1]):
            path.append(st_out.pop())
        else: # top of st_out is right child of root, which is not on the path...pop it
            st_out.pop()
    path.reverse()
    return path

## Visualization

# DEPRACATION WARNING: these draw commands will be removed

# Draw Tree
def _LBT_draw_tree(root):
    def height(root):
        return 1 + max(height(root[DIR_LEFT]), height(root[DIR_RIGHT])) if root else 0
    def jumpto(x, y):
        t.penup()
        t.goto(x, y)
        t.pendown()
    def draw(node, x, y, dx):
        if node:
            t.goto(x, y)
            jumpto(x, y-20)
            t.write(node[VALUE_KEY], align='center', font=('Arial', 12, 'normal'))
            draw(node[DIR_LEFT], x-dx, y-60, dx/2)
            jumpto(x, y-20)
            draw(node[DIR_RIGHT], x+dx, y-60, dx/2)
    # because turtle has this weird behavior that after it closes, you have to run it twice to get it back
    try:
        t = turtle.Turtle()
    except:
        t = turtle.Turtle()
    t.speed(0); turtle.delay(0)
    h = height(root)
    jumpto(0, 30*h)
    draw(root, 0, 30*h, 40*h)
    t.hideturtle()
    turtle.mainloop()

################################# Traversals ##################################
## func must be a function that returns TRAVERSE_GO to continue or TRAVERSE_STOP to return! 
## func must have signature: tree/stack trace of nodes, index/node
## Traversals themselves do not return anything

# _LBT_inorder_traversal(root, func, /, *args, **kwargs)
def _LBT_inorder_traversal(root, func, /, *args, reverse=False, **kwargs):
    if not reverse:
        _DIR_LEADER, _DIR_FOLLOWER = DIR_LEFT, DIR_RIGHT
    else:
        _DIR_LEADER, _DIR_FOLLOWER = DIR_RIGHT, DIR_LEFT
    st = []
    cont_cond = TRAVERSE_GO
    node = root
    while cont_cond and (st or node is not None):
        # go down left side of sub-tree
        while node is not None:
            st.append(node)
            node = node[_DIR_LEADER]
        
        node = st.pop()
        cont_cond = func(st, node, *args, **kwargs)
        node = node[_DIR_FOLLOWER]
        
# _LBT_preorder_traversal(root, func, /, *args, **kwargs)
def _LBT_preorder_traversal(root, func, /, *args, reverse=False, **kwargs):
    if not reverse:
        _DIR_LEADER, _DIR_FOLLOWER = DIR_LEFT, DIR_RIGHT
    else:
        _DIR_LEADER, _DIR_FOLLOWER = DIR_RIGHT, DIR_LEFT
    st = []
    cont_cond = TRAVERSE_GO
    node = root
    st.append(node)
    while cont_cond and st:
        node = st.pop()
        if node is not None:
            cont_cond = func(st, node, *args, **kwargs)
            st.append(node[_DIR_FOLLOWER])
            st.append(node[_DIR_LEADER])
        
# _LBT_postorder_traversal(root, func, /, *args, **kwargs)
def _LBT_postorder_traversal(root, func, /, *args, reverse=False, **kwargs):
    if not reverse:
        _DIR_LEADER, _DIR_FOLLOWER = DIR_LEFT, DIR_RIGHT
    else:
        _DIR_LEADER, _DIR_FOLLOWER = DIR_RIGHT, DIR_LEFT
    cont_cond = TRAVERSE_GO
    node = root
    st = [node]
    while cont_cond:
        node = st.pop()
        # go down left side of sub-tree
        while node is not None:
            if node[_DIR_FOLLOWER] is not None:
                st.append(node[_DIR_FOLLOWER])
            st.append(node)
            node = node[_DIR_LEADER]
        
        node = st.pop()
        while st and st[-1] != node[_DIR_FOLLOWER]:
            cont_cond = func(st, node, *args, **kwargs)
            node = st.pop()
        if st:
            st.pop()
            st.append(node)
            st.append(node[_DIR_FOLLOWER])
        else: # if stack is empty at this point, run last index. This can also go past the outer loop if additionally checked by cont_cond==TRAVERSE_GO
            cont_cond = func(st, node, *args, **kwargs)
            cont_cond = TRAVERSE_STOP     
        
# _LBT_levelorder_traversal(root, func, /, *args, **kwargs)
def _LBT_levelorder_traversal(root, func, /, *args, reverse=False, **kwargs):
    if not reverse:
        _DIR_LEADER, _DIR_FOLLOWER = DIR_LEFT, DIR_RIGHT
    else:
        _DIR_LEADER, _DIR_FOLLOWER = DIR_RIGHT, DIR_LEFT
    cont_cond = TRAVERSE_GO
    node = root
    deq = deque([node])
    while cont_cond and deq:
        node = deq.popleft()
        if node is not None:
            deq.append(node[_DIR_LEADER])
            deq.append(node[_DIR_FOLLOWER])
            cont_cond = func(deq, node, *args, **kwargs)
        
## Traversal for parsing/creating

# There is a copy of _inorder_to_level_order in LinkedBinaryTree.py
def _inorder_to_level_order(arr, /, *, inplace=False, binary_tree_type=BT_BALANCED):
    out = None
    N = len(arr)
    out = []
    if not N:
        return out
    if binary_tree_type == BT_BALANCED:
        deq = deque([(0, N)])
        while deq:
            start, end = deq.popleft()
            if start < N:
                diff = end-start
                if diff > 2:
                    root = _interval_root(start, end)
                    deq.append((start, root))
                    deq.append((root+1, end))
                elif diff == 2:
                    root = start + 1
                    deq.append((start, root))
                    deq.append((N, N))
                elif diff == 1:
                    root = start
                    deq.append((N, N))
                    deq.append((N, N))
                out.append(arr[root])
            else:
                out.append(None)
        
        while out and out[-1] is None:
            out.pop()
                
        if inplace:
            for i in range(N):
                arr[i] = out[i]
            for i in range(N, len(out)):
                arr.append(out[i])
    elif binary_tree_type == BT_COMPLETE:
        N = len(arr)
        if not N:
            return []
        out = [None]*N
        path = []
        i = 0
        node = 0
        while i < N and (node < N or path):
            while node < N:
                path.append(node)
                node = _move(node, DIR_LEFT)
            
            node = path.pop()
            out[node] = arr[i]
            
            i += 1
            node = _move(node, DIR_RIGHT)
                
        if inplace:
            for i in range(N):
                arr[i] = out[i]
    else:
        raise ValueError(f"binary tree to level order does not support creation to binary tree type {binary_tree_type}")
    return out
        
################################# Public API ##################################

## Creation

# root = LBT_create(contents, /, *, inplace=False, binary_tree_type='balanced' : 'complete') # inplace is not used
def LBT_create(contents, /, *, binary_tree_type=BT_BALANCED, node_factory=DEFAULT_NODE_FACTORY):
    if isinstance(contents, Iterable):
        # function mutates list(contents)
        return _LBT_create_from_sequence(list(contents), binary_tree_type=binary_tree_type, node_factory=node_factory)
    else:
        return node_factory(contents)

## Tree properties/geometry

LBT_size = _LBT_size
LBT_height = _LBT_height
LBT_depth = _LBT_depth

## Tree contents/queries/traversals

# multiple dispatch might also work here, but we cannot do it by argument type
# LBT_traverse(root, func, *args, traversal=TRAVERSE_INORDER, **kwargs) # for first release, if func=None, *args are ignored
def LBT_traverse(root, func, *args, traversal=TRAVERSE_INORDER, reverse=False, **kwargs):
    if traversal == TRAVERSE_INORDER:
        _LBT_inorder_traversal(root, func, *args, reverse=reverse, **kwargs)
    elif traversal == TRAVERSE_PREORDER:
        _LBT_preorder_traversal(root, func, *args, reverse=reverse, **kwargs)
    elif traversal == TRAVERSE_POSTORDER:
        _LBT_postorder_traversal(root, func, *args, reverse=reverse, **kwargs)
    elif traversal == TRAVERSE_LEVELORDER:
        _LBT_levelorder_traversal(root, func, *args, reverse=reverse, **kwargs)
    else:
        raise ValueError(f"traversal option {traversal} not understood or not implemented for LBTs")
  
# size_t = LBT_count(root, value, /, key=None)
def LBT_count(root, value, /, *, key=None):
    result = [0]
    if key is None:
        def _LBT_count_helper(root, node, value, result):
            if node[VALUE_KEY] == value:
                result[0] += 1
            return TRAVERSE_GO
        LBT_traverse(root, _LBT_count_helper, value, result)
    else:
        def _LBT_count_helper(root, node, value, key, result):
            if key(node[VALUE_KEY]) == value:
                result[0] += 1
            return TRAVERSE_GO
        LBT_traverse(root, _LBT_count_helper, value, key, result)
    return result[0]

# [inorder indices] = _LBT_find(root, value, number=-1, /, *, key=None)
# WARNING: don't use this, subject to change signature; specifically the output
def _LBT_find(root, value, number=-1, /, *, key=None):
    result = []
    counter = [-1]
    if key is None:
        def _LBT_find_helper(root, node, value, number, result, counter):
            counter[0] += 1
            if node[VALUE_KEY] == value:
                result.append(counter[0])
                if len(result) == number:
                    return TRAVERSE_STOP
            return TRAVERSE_GO
        LBT_traverse(root, _LBT_find_helper, value, number, result, counter)
    else:
        def _LBT_find_helper(root, node, value, key, number, result, counter):
            counter[0] += 1
            if key(node[VALUE_KEY]) == value:
                result.append(counter[0])
                if len(result) == number:
                    return TRAVERSE_STOP
            return TRAVERSE_GO
        LBT_traverse(root, _LBT_find_helper, value, key, number, result, counter)
    return result

# boolean = _LBT_contains(root, value, /, *, key=None)
def LBT_contains(root, value, /, *, key=None):
    return len(_LBT_find(root, value, 1, key=key)) > 0

## Tree mutations

# new_root = LBT_add(root, value, /)
def LBT_add(root, value, /, node_factory=DEFAULT_NODE_FACTORY):
    result = []
    def _LBT_find_open_node(root, node, result):
        if node[DIR_LEFT] is None:
            result.append((node, DIR_LEFT))
            return TRAVERSE_STOP
        if node[DIR_RIGHT] is None:
            result.append((node, DIR_RIGHT))
            return TRAVERSE_STOP
        return TRAVERSE_GO
    LBT_traverse(root, _LBT_find_open_node, result, traversal=TRAVERSE_LEVELORDER)
    node, dir_ = result.pop()
    child = node_factory(value)
    node[dir_] = child
    return root

# new_root = LBT_remove(root, value, /, *, key=None) # raises KeyError if not found
def LBT_remove(root, value, /, *, key=None):
    path = _LBT_path_to(root, value, key=key)
    if not path:
        raise KeyError(f"LBT_remove: key {value} not found in tree")
    node = path.pop()
    
    if _LBT_is_leaf(node):
        if path:
            parent = path.pop()
            dir_ = DIR_LEFT if node is parent[DIR_LEFT] else DIR_RIGHT
            parent[dir_] = None
            del node
            return root
        else: # node is root and it is a leaf...destroy the root
            root = None
            return root
    
    left_max_path, left_min_path = _LBT_extremal_paths_to_leaves(node[DIR_LEFT])
    right_max_path, right_min_path = _LBT_extremal_paths_to_leaves(node[DIR_LEFT])
    
    if len(left_max_path) > len(right_max_path):
        # remove from left subtree
        replacement = left_max_path.pop()
        if left_max_path[-1][DIR_LEFT] is replacement:
            left_max_path[-1][DIR_LEFT] = None
        else:
            left_max_path[-1][DIR_RIGHT] = None
    else: 
        # remove from right subtree
        replacement = right_max_path.pop()
        if right_max_path[-1][DIR_LEFT] is replacement:
            right_max_path[-1][DIR_LEFT] = None
        else:
            right_max_path[-1][DIR_RIGHT] = None
    replacement[VALUE_KEY], node[VALUE_KEY] = node[VALUE_KEY], replacement[VALUE_KEY]
    del replacement
    return root

# new_root = LBT_discard(root, value, /, *, key=None, parent=None) # wrapper for _LBT_remove that catches KeyError
def LBT_discard(root, value, /, *, key=None):
    try:
        return LBT_remove(root, value, key=key)
    except KeyError:
        return root

# bool = LBT_equals(root1, root2, /)
def LBT_equals(root1, root2):
    if root1 is None or root2 is None:
        return root1 == root2
    return root1[VALUE_KEY] == root2[VALUE_KEY] and LBT_equals(root1[DIR_LEFT]) and LBT_equals(root2[DIR_RIGHT])