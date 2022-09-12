# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 18:39:40 2022

@author: jeffr
"""

from collections import deque # for traversals
from collections.abc import Iterable
from dtlib.utils import _next_pow2, _interval_root
import dtlib.trees._Node as _Node
from dtlib.trees._constants import VALUE_KEY, DIR_LEFT, DIR_RIGHT, \
    DIR_PARENT, BT_BALANCED, BT_COMPLETE, TRAVERSE_GO, \
    TRAVERSE_STOP, TRAVERSE_INORDER, TRAVERSE_PREORDER, \
    TRAVERSE_POSTORDER, TRAVERSE_LEVELORDER, LIST_NODE
#from BLib.Trees import BinaryTree as BT
import turtle # to be removed

# TODO: create iterator classes for each type of iteration
# TODO: Iterable = ABT_iter(tree, /, *, traversal='inorder')
# TODO: Note that BinarySearchTree

############################## Module globals ################################

## utilizing BLib.Trees._constants

DEFAULT_NODE_FACTORY = _Node.Node_factory(LIST_NODE)

################################ UTILITIES ####################################

## Node properties

def _ABT_is_leaf(tree, index, /):
    N = len(tree)
    if index < N and tree[index] is not None:
        child = _move(index, DIR_LEFT)
        if child >= N or tree[child] is None:
            child = _move(index, DIR_RIGHT)
            if child >= N or tree[child] is None:
                return True
    return False

## Navigation

def _ABT_move_index(index, dir_, /):
    if dir_ == DIR_PARENT:
        return ((index-1) >> 1)
    #return (index << 1) + 1 + dir_ # depends on DIR_LEFT = 0
    return (index << 1) + (1 if dir_==DIR_LEFT else 2)

_move = _ABT_move_index

## Tree properties/geometry

# size_t = _ABT_size(tree, index=0, /)
def _ABT_size(tree, index=0, /):
    if index >= len(tree) or tree[index] is None:
        return 0
    return 1 + _ABT_size(tree, _move(index, DIR_LEFT)) + _ABT_size(tree, _move(index, DIR_RIGHT))

def _ABT_diameter_helper(tree, index, /):
    if index >= len(tree) or tree[index] is None:
        return 0, 0
    l_max_diameter, l_height = _ABT_diameter_helper(tree, _move(index, DIR_LEFT))
    r_max_diameter, r_height  = _ABT_diameter_helper(tree, _move(index, DIR_RIGHT))
    return max(l_max_diameter, r_max_diameter, 1 + l_height + r_height), 1 + max(l_height, r_height)

# size_t = _ABT_diameter(tree, index=0, /)    
def _ABT_diameter(tree, index=0, /):
    if not tree or index >= len(tree) or tree[index] is None:
        return 0
    return _ABT_diameter_helper(tree, index)[0]

# O(logN)
# size_t = _ABT_depth(tree, index, /)
def _ABT_depth(tree, index=0, /):
    if not tree or index >= len(tree) or tree[index] is None:
        return 0
    depth = 0
    while index >= 0:
        index = _move(index, DIR_PARENT)
        depth += 1
    return depth

# size_t = _ABT_height(tree, index=0, /)
def _ABT_height(tree, index=0, /):
    #print(tree)
    if not tree or index >= len(tree) or tree[index] is None:
        return 0
    return 1 + max(_ABT_height(tree, _move(index, DIR_LEFT)), _ABT_height(tree, _move(index, DIR_RIGHT)))

## Tree manipulation

# WARNING: swap does not check to ensure that the tree pre/post maintains structure invariants
def _ABT_swap(tree, index1, index2):
    tree[index1], tree[index2] = tree[index2], tree[index1]
    
def _ABT_value_swap(tree, index1, index2):
    tree[index1][VALUE_KEY], tree[index2][VALUE_KEY] = tree[index2][VALUE_KEY], tree[index1][VALUE_KEY]
    
def _ABT_extend(tree, Ntarget, /):
    N = len(tree)
    if Ntarget > N:
        tree.extend([None]*(Ntarget-N))

# time is 2 * N where N is the size of the subtree located at root_index
def _ABT_move_subtree(tree, root, target, /):
    N = len(tree)
    if root >= N or tree[root] is None:
        # not sure why I put this here...leaving it commented. If root >= N but target < N, that's equivalent to trying to delete by moving out of bounds...do not want that
        #if target < N:
        #    tree[target] = None
        return
    
    if target > root: # shift down or parallel right
        Ncur = N
        # perform a reverse postorder traversal of the subtree tree (reverse meaning right, left, then root as opposed to left, right, then root)
        # as this is a nonstandard traversal and I need to modify the tree while traversing, it is custom and not reusing code I already have
        # in principle this can be done with a standard postorder traversal, but this loop makes a lot more sense to me
        st_visit = []
        st_traverse = [(root, target)]
        
        # find if target is in the left subtree or to the left of root
        parent = target
        left = _move(root, DIR_LEFT)
        rightmost_left_level = _next_pow2(left+1)-2
        while parent > rightmost_left_level:
            parent = _move(parent, DIR_PARENT)
        if parent > left: # target is to the right of the root
            while st_traverse:
                # note that N cannot change while traversing! That's why we have Ncur
                if st_traverse[-1][0] < N and tree[st_traverse[-1][0]] is not None:
                    st_visit.append(st_traverse.pop())
                    
                    root = _move(st_visit[-1][0], DIR_LEFT) # move to left child of source
                    target = _move(st_visit[-1][-1], DIR_LEFT) # move to left child of destination
                    st_traverse.append((root, target)) # add left children to traversal stack
                    
                    root += DIR_RIGHT - DIR_LEFT # move to right child of source
                    target += DIR_RIGHT - DIR_LEFT # move to right child of destination
                    st_traverse.append((root, target)) # add right children to traversal stack
                else:
                    st_traverse.pop()
                    while st_visit and (not st_traverse or st_visit[-1][0] > st_traverse[-1][0]):
                        if st_visit[-1][1] >= Ncur:
                            # this next line is why I cannot do a traditional traversal, which is stable only if the underlying tree is NOT modified
                            _ABT_extend(tree, st_visit[-1][1] + 1) # this could get very expensive if it has to be executed multiple times, but in a rotation, this should happen only once if the tree structures maintains a "complete" size and maybe 2x otherwise.
                            Ncur = len(tree)
                        _ABT_swap(tree, *st_visit.pop())
        else:
            while st_traverse:
                # note that N cannot change while traversing! That's why we have Ncur
                if st_traverse[-1][0] < N and tree[st_traverse[-1][0]] is not None:
                    st_visit.append(st_traverse.pop())
                    
                    root = _move(st_visit[-1][0], DIR_RIGHT) # move to right child of source
                    target = _move(st_visit[-1][-1], DIR_RIGHT) # move to right child of destination
                    st_traverse.append((root, target)) # add right children to traversal stack
                    
                    root -= DIR_RIGHT - DIR_LEFT # move to left child of source
                    target -= DIR_RIGHT - DIR_LEFT # move to left child of destination
                    st_traverse.append((root, target)) # add left children to traversal stack
                else:
                    st_traverse.pop()
                    while st_visit and (not st_traverse or st_visit[-1][0] > st_traverse[-1][0]):
                        if st_visit[-1][1] >= Ncur:
                            # this next line is why I cannot do a traditional traversal, which is stable only if the underlying tree is NOT modified
                            _ABT_extend(tree, st_visit[-1][1] + 1) # this could get very expensive if it has to be executed multiple times, but in a rotation, this should happen only once if the tree structures maintains a "complete" size and maybe 2x otherwise.
                            Ncur = len(tree)
                        _ABT_swap(tree, *st_visit.pop())
                
    elif target < root: # shift up or parallel left
        if target < 0:
            raise ValueError(f"cannot move subtree to negative root index {target}")
            
        # perform a preorder traversal of the tree moving subtree elements at root_index to subtree rooted at target_index
        deq_traverse = deque([(root, target)])
        while deq_traverse:
            src, dest = deq_traverse.popleft()
            if src < N and tree[src] is not None: 
                _ABT_swap(tree, src, dest) # swap source and destination
                
                root = _move(src, DIR_RIGHT) # move to right child of source
                target = _move(dest, DIR_RIGHT) # move to right child of destination
                deq_traverse.append((root, target)) # add right children to traversal deque
                
                root += DIR_LEFT - DIR_RIGHT # move to left child of source
                target += DIR_LEFT - DIR_RIGHT # move to right child of destination
                deq_traverse.append((root, target)) # add left children to traversal deque
    return # else do nothing because it's not moving

# tree = _ABT_rotate(tree, index, dir_, /)
# rotate the node represented by tree[index] in dir_ direction
# complexity. For a tree of size N and a subtree rooted at index of size M, this is O(M) in time complexity and max(O(N)) in space
def _ABT_rotate(tree, index, dir_, /):
    N = len(tree)
    if index >= N or tree[index] is None:
        return # do nothing because it cannot be rotated or rotating is meaningless
    
    left_child = _move(index, DIR_LEFT)
    right_child = _move(index, DIR_RIGHT)
    
    if dir_ == DIR_LEFT:
        if right_child >= N or tree[right_child] is None: # cannot rotate left
            return

        # move index's left child subtree down to its left # down and left move
        _ABT_move_subtree(tree, left_child, _move(left_child, DIR_LEFT))

        #tree[left_child] = None # clear the position. should not be necessary
        # swap index to its left child position
        _ABT_swap(tree, index, left_child)

        # move index's right child's left subtree to index's left child's right subtree # left move
        _ABT_move_subtree(tree, _move(right_child, DIR_LEFT), _move(left_child, DIR_RIGHT))

        # swap index's right child to index
        _ABT_swap(tree, index, right_child)

        # move index's right child's right subtree up to index's right subtree # up and left move
        _ABT_move_subtree(tree, _move(right_child, DIR_RIGHT), right_child)

    elif dir_ == DIR_RIGHT:
        if left_child >= N or tree[left_child] is None: # cannot rotate right
            return
        # if rotating right, the swaps require AT LEAST a tree of size right_child + 1
        if right_child >= N:
            _ABT_extend(tree, right_child+1)
        # move index's right child down to its right # down and right move
        _ABT_move_subtree(tree, right_child, _move(right_child, DIR_RIGHT))
        
        # swap index to its right child position
        _ABT_swap(tree, index, right_child)
        
        # move index's left child's right subtree to index's right child's left subtree # right move
        _ABT_move_subtree(tree, _move(left_child, DIR_RIGHT), _move(right_child, DIR_LEFT))
        
        # swap index's left child to index
        _ABT_swap(tree, index, left_child)
        
        #move index's left child's left subtree up to index's left subtree # up and right
        _ABT_move_subtree(tree, _move(left_child, DIR_LEFT), left_child)
        
    else:
        raise ValueError(f"rotation direction {dir_} in _ABT_rotate not understood")
        
    return tree

# tree = _ABT_split_rotate(tree, index, dir_, /) # optimization on double rotations
# perform split rotation as defined in Nievergelt 1973. This is obviously meant for weight-balanced trees, but is still generally applicable to binary trees
# this is a separate function because we are dealing with array representations and performing a "double-rotation" or two successive rotations is unnecessarily inefficients
# The way this is implemented, it's a bit of a misnomer to call it a rotation. A grandchild subtree is promoted to the root after pushing the root down

# a double rotation would result in O(3*M/2) movements in data for a subtree of size M rooted at M, the split rotation below uses O(3*M/4) or half as much overhead
# there is a risk that we still trigger the O(N) increase in memory and time complexity if the subtree in dir_ is full height
def _ABT_split_rotate(tree, index, dir_, /):
    N = len(tree)
    if index >= N or tree[index] is None:
        return # do nothing because it cannot be rotated or rotating is meaningless
    
    left_child = _move(index, DIR_LEFT)
    right_child = _move(index, DIR_RIGHT)
    
    if dir_ == DIR_LEFT:
        grandchild = _move(right_child, DIR_LEFT)
        if right_child >= N or grandchild >= N or tree[right_child] is None or tree[grandchild] is None: # cannot rotate left
            return
        # move left_child to its left subtree # might incur O(N) memory increase and build time
        _ABT_move_subtree(tree, left_child, _move(left_child, DIR_LEFT))
        
        # swap index and left_child
        _ABT_swap(tree, index, left_child)
        
        # swap grandchild and index
        _ABT_swap(tree, index, grandchild)
        
        # move grandchild's left subtree to left_child's right subtree
        _ABT_move_subtree(tree, _move(grandchild, DIR_LEFT), _move(left_child, DIR_RIGHT))
        
        # move granchild's right subtree to right_child's left subtree
        _ABT_move_subtree(tree, _move(grandchild, DIR_RIGHT), _move(right_child, DIR_LEFT))
        
    elif dir_ == DIR_RIGHT:
        grandchild = _move(left_child, DIR_RIGHT)
        if left_child >= N or grandchild >= N or tree[left_child] is None or tree[grandchild] is None: # cannot rotate right
            return
        if grandchild >= N:
            _ABT_extend(tree, grandchild+1)
        
        # move right_child to its right subtree # might incur O(N) memory increase and build time
        _ABT_move_subtree(tree, right_child, _move(right_child, DIR_RIGHT))
        # swap index and right_child
        _ABT_swap(tree, index, right_child)
        # swap grandchild and index
        _ABT_swap(tree, index, grandchild)
        # move granchild's right subtree to right_child's left subtree
        _ABT_move_subtree(tree, _move(grandchild, DIR_RIGHT), _move(right_child, DIR_LEFT))
        # move grandchild's left subtree to left_child's right subtree
        _ABT_move_subtree(tree, _move(grandchild, DIR_LEFT), _move(left_child, DIR_RIGHT))
        
    else:
        raise ValueError(f"rotation direction {dir_} in _ABT_rotate not understood")
    
    return tree

## Internal queries

# index, size_t = _ABT_leftmost(tree, index=0, /)
def _ABT_leftmost(tree, index=0, /, *, path=None):
    if path is None:
        path = []
    N = len(tree)
    while index < N and tree[index] is not None:
        path.append(index)
        index = _move(index, DIR_LEFT)
    return path[-1], len(path)-1
    """
    depth = 0
    left = _move(index, DIR_LEFT)
    while left < N and tree[left] is not None:
        
        depth += 1
        index, left = left, _move(left, DIR_LEFT)
    return index, depth
    """

# index, size_t = _ABT_leftmost(tree, index=0, /)
def _ABT_rightmost(tree, index=0, /, *, path=None):
    if path is None:
        path = []
    N = len(tree)
    while index < N and tree[index] is not None:
        path.append(index)
        index = _move(index, DIR_RIGHT)
    return path[-1], len(path)-1
    """
    depth = 0
    right = _move(index, DIR_RIGHT)
    while right < N and tree[right] is not None:
        depth += 1
        index, right = right, _move(right, DIR_RIGHT)
    return index, depth
    """

# index to leaf = _ABT_extremal_paths_to_leaves(tree, index, /)
# not sure this is useful
def _ABT_extremal_paths_to_leaves(tree, index=0, /):
    if index >= len(tree) or tree[index] is None:
        return None, None
    
    left_max, left_min = _ABT_extremal_paths_to_leaves(tree, _move(index, DIR_LEFT))
    right_max, right_min = _ABT_extremal_paths_to_leaves(tree, _move(index, DIR_RIGHT))
    if left_max is None and right_max is None: # node tree[index] is a leaf
        return index, index
    elif right_max is None: # left is not None
        return left_max, left_min
    elif left_max is None: # right is not None
        return right_max, right_min
    
    return max(left_max, right_max), min(left_min, right_min)

# [path of indices] = _ABT_path_to(tree, value, /, *, key=None)
def _ABT_path_to(tree, value, /, *, key=None):
    st_out = [] # not really a stack; it's going to be the index for an occurrence of value
    if key is None:
        def _ABT_path_to_helper(tree, index, value, st_out):
            if tree[index][VALUE_KEY] == value:
                st_out.append(index)
                return TRAVERSE_STOP
            return TRAVERSE_GO
        ABT_traverse(tree, _ABT_path_to_helper, value, st_out, traversal=TRAVERSE_POSTORDER)
    else:
        def _ABT_path_to_helper(tree, index, value, st_out, key):
            if key(tree[index][VALUE_KEY]) == value:
                st_out.append(index)
                return TRAVERSE_STOP
            return TRAVERSE_GO
        ABT_traverse(tree, _ABT_path_to_helper, value, st_out, key, traversal=TRAVERSE_POSTORDER)  
    if st_out:
        while st_out[-1] >= 0:
            st_out.append(_move(st_out[-1], DIR_PARENT))
        st_out.pop()
    st_out.reverse()
    return st_out

## Visualization

# DEPRACATION WARNING: these draw commands will be removed

# Draw Tree
def _ABT_draw_tree(tree):
    def jumpto(x, y):
        t.penup()
        t.goto(x, y)
        t.pendown()
    def draw(tree, index, x, y, dx):
        if index < len(tree) and tree[index] is not None:
            t.goto(x, y)
            jumpto(x, y-20)
            t.write(tree[index][VALUE_KEY], align='center', font=('Arial', 12, 'normal'))
            draw(tree, _move(index, DIR_LEFT), x-dx, y-60, dx/2)
            jumpto(x, y-20)
            draw(tree, _move(index, DIR_RIGHT), x+dx, y-60, dx/2)
    # because turtle has this weird behavior that after it closes, you have to run it twice to get it back
    try:
        t = turtle.Turtle()
    except:
        t = turtle.Turtle()
    t.speed(0); turtle.delay(0)
    h = _ABT_height(tree)
    jumpto(0, 30*h)
    draw(tree, 0, 0, 30*h, 40*h)
    t.hideturtle()
    turtle.mainloop()

################################# Traversals ##################################
## func must be a function that returns TRAVERSE_GO to continue or TRAVERSE_STOP to return! 
## func must have signature: tree/stack trace of nodes, index/node
## Traversals themselves do not return anything

# _ABT_inorder_traversal(tree, func, /, *args, **kwargs)
def _ABT_inorder_traversal(tree, func, /, *args, reverse=False, **kwargs):
    if not reverse:
        _DIR_LEADER, _DIR_FOLLOWER = DIR_LEFT, DIR_RIGHT
    else:
        _DIR_LEADER, _DIR_FOLLOWER = DIR_RIGHT, DIR_LEFT
    st = []
    index = 0
    N = len(tree)
    cont_cond = TRAVERSE_GO
    while cont_cond and (st or (index < N and tree[index] is not None)):
        # go down left side of sub-tree
        while index < N and tree[index] is not None:
            st.append(index)
            index = _move(index, _DIR_LEADER)
        
        index = st.pop()
        cont_cond = func(tree, index, *args, **kwargs)
        index = _move(index, _DIR_FOLLOWER)
        
# _ABT_preorder_traversal(tree, func, /, *args, **kwargs)
def _ABT_preorder_traversal(tree, func, /, *args, reverse=False, **kwargs):
    if not reverse:
        _DIR_LEADER, _DIR_FOLLOWER = DIR_LEFT, DIR_RIGHT
    else:
        _DIR_LEADER, _DIR_FOLLOWER = DIR_RIGHT, DIR_LEFT
    st = []
    N = len(tree)
    index = 0
    cont_cond = TRAVERSE_GO
    st.append(index)
    while cont_cond and st:
        index = st.pop()
        if index < N and tree[index] is not None:
            cont_cond = func(tree, index, *args, **kwargs)
            st.append(_move(index, _DIR_FOLLOWER))
            st.append(_move(index, _DIR_LEADER))
        
# _ABT_postorder_traversal(tree, func, /, *args, **kwargs)
# the trick to avoid O(N) memory is to actually traverse as preorder. as you
# are popping off the traversal stack, if the next value is the current node's
# right now, flip their order
def _ABT_postorder_traversal(tree, func, /, *args, reverse=False, **kwargs):
    if not reverse:
        _DIR_LEADER, _DIR_FOLLOWER = DIR_LEFT, DIR_RIGHT
    else:
        _DIR_LEADER, _DIR_FOLLOWER = DIR_RIGHT, DIR_LEFT
    index = 0
    st = [index]
    N = len(tree)
    cont_cond = TRAVERSE_GO
    while cont_cond:
        index = st.pop()
        # go down left side of sub-tree
        while index < N and tree[index] is not None:
            right = _move(index, _DIR_FOLLOWER)
            if right < N and tree[right] is not None:
                st.append(right)
            st.append(index)
            index = _move(index, _DIR_LEADER)
        
        index = st.pop()
        right =  _move(index, _DIR_FOLLOWER)
        while st and st[-1] != right:
            cont_cond = func(tree, index, *args, **kwargs)
            index = st.pop()
            right = _move(index, _DIR_FOLLOWER)
        if st:
            right = st.pop()
            st.append(index)
            st.append(right)
        else: # if stack is empty at this point, run last index. This can also go past the outer loop if additionally checked by cont_cond==TRAVERSE_GO
            cont_cond = func(tree, index, *args, **kwargs)
            cont_cond = TRAVERSE_STOP
        
# _ABT_levelorder_traversal(tree, func, /, *args, **kwargs)
# this is a lot simplier if reverse=False
def _ABT_levelorder_traversal(tree, func, /, *args, reverse=False, **kwargs):
    index = 0
    cont_cond = TRAVERSE_GO
    N = len(tree)
    level_size = 1
    level_start_index = 0
    if reverse:
        delta = -1
    else:
        delta = 1
    while cont_cond and index < N:
        if tree[index] is not None:
            cont_cond = func(tree, index, *args, **kwargs)
        if reverse and index == level_start_index:
            level_start_index += level_size
            if level_start_index < N:
                level_size <<= 1
                index = min(N, level_start_index + level_size)
            else:
                index = N+1
        index += delta 
        
## Traversal for parsing/creating

# There is a copy of _inorder_to_level_order in ArrayBinaryTree.py
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

# tree = ABT_create(contents, /, *, None, inplace=False, binary_tree_type='balanced' : 'complete', node_factory=None) # node_factory is not used
# does a shallow copy of contents if Iterable and not inplace
# node_factory is only meant for specializations that actually requires nodes. For simple BSTs, do not use node_factory unless you correct the key parameters for the node structure
def ABT_create(contents=None, Nmin=0, /, *, inplace=False, binary_tree_type=BT_BALANCED, node_factory=DEFAULT_NODE_FACTORY):
    if contents is None:
        return [None]*Nmin
    
    if isinstance(contents, Iterable):
        if inplace:
            if not isinstance(contents, list):
                raise ValueError("cannot create an ABT in place with non-list contents")
            else:
                pass # contents is already a list that can be modified
        else:
            contents = list(contents)
    else:
        contents = [contents]
    
    if inplace:
        _inorder_to_level_order(contents, inplace=True, binary_tree_type=binary_tree_type)
    else:
        contents = _inorder_to_level_order(contents, inplace=False, binary_tree_type=binary_tree_type)
    
    # extension only makes sense if already in level order
    N = len(contents)
    # CONSIDER: working in the application of node_factory into _inorder_to_level_order so that node creation happens at the same time as filling contents
    #   would cut down overhead by factor of 2, but then there would maybe be differences between the Linked version and the Array version
    if node_factory is not None:
        for i in range(N):
            if contents[i] is not None:
                contents[i] = node_factory(contents[i])
    if Nmin > N:
        contents.extend([None]*(Nmin-N))
    return contents

## Tree properties/geometry

ABT_size = _ABT_size
ABT_height = _ABT_height
ABT_depth = _ABT_depth

## Tree contents/queries/traversals

# multiple dispatch might also work here, but we cannot do it by argument type
# ABT_traverse(tree, func, *args, traversal=TRAVERSE_INORDER, **kwargs) # for first release, if func=None, *args are ignored
def ABT_traverse(tree, func, *args, traversal=TRAVERSE_INORDER, reverse=False, **kwargs):
    if traversal == TRAVERSE_INORDER:
        _ABT_inorder_traversal(tree, func, *args, reverse=reverse, **kwargs)
    elif traversal == TRAVERSE_PREORDER:
        _ABT_preorder_traversal(tree, func, *args, reverse=reverse, **kwargs)
    elif traversal == TRAVERSE_POSTORDER:
        _ABT_postorder_traversal(tree, func, *args, reverse=reverse, **kwargs)
    elif traversal == TRAVERSE_LEVELORDER:
        _ABT_levelorder_traversal(tree, func, *args, reverse=reverse, **kwargs)
    else:
        raise ValueError(f"traversal option {traversal} not understood or not implemented for ABTs")

# size_t = ABT_count(tree, value, /, key=None)
def ABT_count(tree, value, /, *, key=None):
    result = [0]
    if key is None:
        def _ABT_count_helper(tree, index, value, result):
            if tree[index][VALUE_KEY] == value:
                result[0] += 1
            return TRAVERSE_GO
        ABT_traverse(tree, _ABT_count_helper, value, result)
    else:
        def _ABT_count_helper(tree, index, value, key, result):
            if key(tree[index][VALUE_KEY]) == value:
                result[0] += 1
            return TRAVERSE_GO
        ABT_traverse(tree, _ABT_count_helper, value, key, result)
    return result[0]

# [inorder indices] = _ABT_find(tree, value, all_=True, /, *, key=None)
# TODO: add reverse
# WARNING: don't use this, subject to change signature; specifically the output
def _ABT_find(tree, value, number=-1, /, *, key=None):
    result = []
    counter = [-1]
    if key is None:
        def _ABT_find_helper(tree, index, value, number, result, counter):
            counter[0] += 1
            if tree[index][VALUE_KEY] == value:
                result.append(counter[0])
                if len(result) == number:
                    return TRAVERSE_STOP
            return TRAVERSE_GO
        ABT_traverse(tree, _ABT_find_helper, value, number, result, counter)
    else:
        def _ABT_find_helper(tree, index, value, key, number, result, counter):
            counter[0] += 1
            if key(tree[index][VALUE_KEY]) == value:
                result.append(counter[0])
                if len(result) == number:
                    return TRAVERSE_STOP
            return TRAVERSE_GO
        ABT_traverse(tree, _ABT_find_helper, value, key, number, result, counter)
    return result

# boolean = _ABT_contains(tree, value, /, *, key=None)
def ABT_contains(tree, value, /, *, key=None):
    return len(_ABT_find(tree, value, 1, key=key)) > 0

## Tree mutations

# tree = ABT_add(tree, value, /)
# node_factory is only meant for specializations that actually requires nodes. For simple BSTs, do not use node_factory unless you correct the key parameters for the node structure
def ABT_add(tree, value, /, *, node_factory=DEFAULT_NODE_FACTORY):
    result = []
    N = len(tree)
    def _ABT_find_open_node(tree, index, end, result):
        child = _move(index, DIR_LEFT)
        if child >= end or tree[child] is None:
            result.append(child)
            return TRAVERSE_STOP
        child = _move(index, DIR_RIGHT)
        if child >= end or tree[child] is None:
            result.append(child)
            return TRAVERSE_STOP
        return TRAVERSE_GO
    ABT_traverse(tree, _ABT_find_open_node, N, result, traversal=TRAVERSE_LEVELORDER)
    index = result.pop()
    if index >= N:
        _ABT_extend(tree, index+1)
    if node_factory is None:
        tree[index] = value
    else:
        tree[index] = node_factory(value)
    return tree

# tree = ABT_remove(tree, value, /, *, key=None) # raises KeyError if not found
# removes element by finding the element and then swaping it with the element
# furthest from its position and then deleting the node. This keeps sibling tree
# structures the same but brings tree more balanced. Unfortunately, this method
# is meaningless for any of the specialized trees that would inherit from
# Binary Tree
def ABT_remove(tree, value, /, *, key=None):
    path = _ABT_path_to(tree, value, key=key)
    if not path:
        raise KeyError(f"ABT_remove: key {value} not found in tree")
    index = path.pop()
    
    if _ABT_is_leaf(tree, index):
        if path:
            tree[index] = None
            return tree
        else: # node is root and it is a leaf...destroy the root
            tree.clear()
            return tree
    
    left_max_path, left_min_path = _ABT_extremal_paths_to_leaves(tree, index)
    right_max_path, right_min_path = _ABT_extremal_paths_to_leaves(tree, index)
    
    if left_max_path > right_max_path:
        # remove from left subtree
        replacement = left_max_path
    else: 
        # remove from right subtree
        replacement = right_max_path
    _ABT_swap(tree, index, replacement) # node to delete is now at replacement
    tree[replacement] = None
    return tree

# tree = ABT_discard(tree, value, /, *, key=None) # wrapper for _ABT_remove that catches KeyError
def ABT_discard(tree, value, /, *, key=None):
    try:
        return ABT_remove(tree, value, key=key)
    except KeyError:
        return tree

def ABT_equals(tree1, tree2):
    N1, N2 = len(tree1), len(tree2)
    if N1 < N2:
        # tree1 should always be at least as big as tree2
        return ABT_equals(tree2, tree1)
    
    i = 0
    while i < N2:
        if tree1[i] != tree2[i]:
            return False
        i += 1
    while i < N1:
        if tree1[i] is not None:
            return False
        i += 1
    return True
