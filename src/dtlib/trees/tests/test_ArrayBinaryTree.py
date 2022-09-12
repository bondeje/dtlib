# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 18:00:58 2022

@author: jeffr
"""

import dtlib.trees._ArrayBinaryTree as BT
from unittest import TestCase as TC
import random
from dtlib.utils import _next_pow2

N = None

class test_ABT(TC):
    @classmethod
    def setUpClass(cls):
        cls.trees = [[(0,),    (1,)],
                     [(0,),    N, (2,)], 
                     [(0,),    (1,),(2,)], 
                     [(0,),    (1,),(2,),    (3,),(4,),(5,),(6,)],
                     [(0,),    (1,), N,    (3,),(4,)],
                     [(0,),    N, (2,),    N, N,(5,),(6,)], 
                     [(0,),    (1,), (2,),    (3,),N,(5,),(6,),    N, N, N, N, (11,)],
                     [(0,),    (1,), (2,),    (3,),(4,),N,N,    (7,),(8,),(9,),N,N,N,N,N,    (15,),(16,),N,N,N,N,N,N,N,N,N,N,N,N,N,N,    (31,)]]
        cls.leaves = [{(1,)}, 
                      {(2,)},
                      {(1,), (2,)},
                      {(3,), (4,), (5,), (6,)},
                      {(3,), (4,)},
                      {(5,), (6,)},
                      {(3,), (6,), (11,)},
                      {(2,), (8,), (9,), (16,), (31,)}]

    def test_ABT_swap(self):
        for i, tree in enumerate(self.trees):
            N = len(tree)
            ind1 = random.randrange(0, N)
            while tree[ind1] is N:
                ind1 = random.randrange(0, N)
            ind2 = random.randrange(0, N)
            while tree[ind2] is N or ind2 == ind1:
                ind2 = random.randrange(0, N)
            old1, old2 = tree[ind1], tree[ind2]
            BT._ABT_swap(tree, ind1, ind2)
            self.assertEqual(old1, tree[ind2], f"{ind1} and {ind2} did not swap in tree[{i}]")
            self.assertEqual(old2, tree[ind1], f"{ind1} and {ind2} did not swap in tree[{i}]")
            
            # reset to original tree
            BT._ABT_swap(tree, ind1, ind2)
            self.assertEqual(old1, tree[ind1], f"{ind2} and {ind1} did not swap in tree[{i}]")
            self.assertEqual(old2, tree[ind2], f"{ind2} and {ind1} did not swap in tree[{i}]")
            
    def test_ABT_extend(self):
        for i, tree in enumerate(self.trees):
            N = len(tree)
            Ntarget = _next_pow2(N)-1
            BT._ABT_extend(tree, Ntarget)
            self.assertEqual(len(tree), Ntarget, f"tree[{i}] did not extend from {N} to {Ntarget}")
            for j in range(N, Ntarget):
                self.assertIsNone(tree[j], f"tree[{i}][{j}] was not initialized to N in extending")
            while len(tree) > N:
                tree.pop()
                
    def test_ABT_move_index(self):
        cases = [(0, BT.DIR_PARENT, -1),
                 (2, BT.DIR_PARENT, 0),
                 (3, BT.DIR_PARENT, 1),
                 (5, BT.DIR_PARENT, 2),
                 (0, BT.DIR_LEFT, 1),
                 (0, BT.DIR_RIGHT, 2),
                 (1, BT.DIR_RIGHT, 4),
                 (2, BT.DIR_LEFT, 5)]
        for case in cases:
            self.assertEqual(BT._move(case[0], case[1]), case[2], f"moving {case[0]} to {'RIGHT' if case[1] == BT.DIR_RIGHT else 'LEFT'} not equal to {case[2]}")
            
    def test_ABT_is_leaf(self):
        for i, leaves in enumerate(self.leaves):
            tree = self.trees[i]
            candidates = leaves.copy()
            for j in range(len(tree)):
                if BT._ABT_is_leaf(tree, j):
                    try:
                        candidates.remove(tree[j]) # throws exception if leaf is found
                    except KeyError:
                        self.assertTrue(False, f"falsely detected trees[{i}] has leaf at {j}: {tree[j]}")
            self.assertSetEqual(candidates, set(), f"failed to detect leaves {candidates} in trees[{i}]")
    
    def test_ABT_equals(self):
        for i in range(len(self.trees)):
            for j in range(len(self.trees)):
                if i != j:
                    self.assertFalse(BT.ABT_equals(self.trees[i], self.trees[j]), f"ABT_equals failed to assert different trees at ({i},{j})")
                else:
                    cpy = self.trees[j].copy()
                    self.assertTrue(BT.ABT_equals(self.trees[i], cpy), f"ABT_equals failed to assert same tree ({i})")
                    cpy.append(N)
                    self.assertTrue(BT.ABT_equals(self.trees[i], cpy), f"ABT_equals failed to assert same tree after appending N at ({i})")
    
    # TODO: Need to test moving a large subtree either here (where I cannot visualize the output since moving a subtree alone will most often result in an invalid binary tree) or rotate
    def test_ABT_move_subtree(self):
        cases = [(0, 1, 2, [(0,),    N,(1,)]),
            (1, 2, 1, [(0,),    (2,),N]),
            (2, 2, 3, [(0,),    (1,),N,    (2,)]),
            (3, 6, 11, [(0,),    (1,),(2,),(3,),(4,),    (5,),N,N,N,N,N,(6,)]),
            #(3, 1, 3, [(0,), N, (2,), (1,), N, (5,), (6, ), (3,), (4,)]), # this was screwing up my rotate
            (4, 4, 2, [(0,),    (1,),(4,),    (3,),N]),
            (5, 6, 1, [(0,),    (6,),(2,),    N,N,(5,),N]),
            (5, 5, 1, [(0,),    (5,),(2,),    N,N,N,(6,)]),
            (6, 11, 4, [(0,),    (1,),(2,),    (3,),(11,),(5,),(6,),    N,N,N,N,N]),
            (6, 11, 7, [(0,),    (1,),(2,),    (3,),N,(5,),(6,),    (11,),N,N,N,N]),
            (6, 11, 8, [(0,),    (1,),(2,),    (3,),N,(5,),(6,),    N,(11,),N,N,N]),
            (6, 2, 4, [(0,),    (1,),N,    (3,),(2,),N,N,    N,N,(5,),(6,),N,N,N,N,    N,N,N,N,(11,)]),
            (7, 1, 3, [(0,),    N,(2,),    (1,),N,N,N,    (3,),(4,),N,N,N,N,N,N,    (7,),(8,),(9,),N,N,N,N,N,N,N,N,N,N,N,N,N,    (15,),(16,),N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,    (31,)]),
            (7, 1, 4, [(0,),    N,(2,),    N,(1,),N,N,    N,N,(3,),(4,),N,N,N,N,    N,N,N,N,(7,),(8,),(9,),N,N,N,N,N,N,N,N,N,    N,N,N,N,N,N,N,N,(15,),(16,),N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,    N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,(31,)]),
            (7, 1, 5, [(0,),    N,(2,),    N,N,(1,),N,    N,N,N,N,(3,),(4,),N,N,    N,N,N,N,N,N,N,N,(7,),(8,),(9,),N,N,N,N,N,    N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,(15,),(16,),N,N,N,N,N,N,N,N,N,N,N,N,N,N,    N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,(31,)]),
            (7, 1, 7, [(0,),    N,(2,),    N,N,N,N,    (1,),N,N,N,N,N,N,N,    (3,),(4,),N,N,N,N,N,N,N,N,N,N,N,N,N,N,    (7,),(8,),(9,),N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,    (15,),(16,),N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,    (31,)])]
        for i, case in enumerate(cases):
            index, src, dest, res = case
            #print('\n'.join(str(c) for c in case) + '\n')
            #BT._ABT_draw_tree(self.trees[index])
            cpy = self.trees[index].copy()
            BT._ABT_move_subtree(cpy, src, dest)
            self.assertTrue(BT.ABT_equals(cpy, res), f"_ABT_move_subtree failed for case {case[:3]}\n{res} and \n{cpy}")
            # undo
            BT._ABT_move_subtree(cpy, dest, src)
            self.assertTrue(BT.ABT_equals(cpy, self.trees[index]), f"_ABT_move_subtree reverse failed for case {case[:3]}\n{self.trees[index]} --> {cpy}")
            
    def test_ABT_rotate(self):
        cases = [(0, 0, BT.DIR_LEFT, [(0,),    (1,)], N), # should not change as it is an illegal rotate
                 (0, 1, BT.DIR_LEFT, [(0,),    (1,)], N), # should not change as it is an illegal rotate
                 (0, 2, BT.DIR_LEFT, [(0,),    (1,)], N), # should not change as it is an illegal rotate
                 (0, 0, BT.DIR_RIGHT, [(1,),    N,(0,)], BT.DIR_LEFT),
                 (1, 0, BT.DIR_LEFT, [(2,),    (0,),N], BT.DIR_RIGHT),
                 (1, 0, BT.DIR_RIGHT, [(0,),    N,(2,)], N), 
                 (1, 1, BT.DIR_RIGHT, [(0,),    N,(2,)], N),
                 (1, 2, BT.DIR_RIGHT, [(0,),    N,(2,)], N),
                 (3, 0, BT.DIR_LEFT, [(2,),    (0,),(6,),    (1,),(5,),N,N,    (3,),(4,)], BT.DIR_RIGHT),
                 (3, 0, BT.DIR_RIGHT, [(1,),    (3,),(0,),    N,N,(4,),(2,),    N,N,N,N,N,N,(5,),(6,)], BT.DIR_LEFT),
                 (4, 0, BT.DIR_RIGHT, [(1,),    (3,),(0,),    N,N,(4,)], BT.DIR_LEFT),
                 (4, 1, BT.DIR_LEFT, [(0,),    (4,),N,    (1,),N,N,N,    (3,)], BT.DIR_RIGHT),
                 (4, 1, BT.DIR_RIGHT, [(0,),    (3,),N,    N,(1,),N,N,    N,N,N,(4,)], BT.DIR_LEFT),
                 (5, 0, BT.DIR_LEFT, [(2,),    (0,),(6,),    N,(5,)], BT.DIR_RIGHT),
                 (5, 2, BT.DIR_LEFT, [(0,),    N,(6,),    N,N,(2,),N,    N,N,N,N,(5,)], BT.DIR_RIGHT),
                 (5, 2, BT.DIR_RIGHT, [(0,),    N,(5,),    N,N,N,(2,),    N,N,N,N,N,N,N,(6,)], BT.DIR_LEFT),
                 (6, 5, BT.DIR_RIGHT, [(0,),    (1,),(2,),    (3,),N,(11,),(6,),    N,N,N,N,N,(5,)], BT.DIR_LEFT),
                 (6, 2, BT.DIR_RIGHT, [(0,),    (1,),(5,),    (3,),N,(11,),(2,),    N,N,N,N,N,N,N,(6,)], BT.DIR_LEFT),
                 (6, 2, BT.DIR_LEFT, [(0,),    (1,),(6,),    (3,),N,(2,),N,    N,N,N,N,(5,),N,N,N,    N,N,N,N,N,N,N,N,(11,)], BT.DIR_RIGHT),
                 (6, 0, BT.DIR_RIGHT, [(1,),    (3,),(0,),    N,N,N,(2,),    N,N,N,N,N,N,(5,),(6,),    N,N,N,N,N,N,N,N,N,N,N,N,(11,)], BT.DIR_LEFT),
                 (7, 0, BT.DIR_LEFT, [(2,),    (0,),N,    (1,),N,N,N,    (3,),(4,),N,N,N,N,N,N,    (7,),(8,),(9,),N,N,N,N,N,N,N,N,N,N,N,N,N,  (15,),(16,),N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,    (31,)], BT.DIR_RIGHT)]
        
        for i, case in enumerate(cases):
            index, node, dir_, res, undo_dir_ = case
            cpy = self.trees[index].copy()
            BT._ABT_rotate(cpy, node, dir_)
            self.assertTrue(BT.ABT_equals(cpy, res), f"_ABT_rotate failed to rotate tree[{index}] around node {node}: {cpy} != {res}")
            if undo_dir_ is not N:
                BT._ABT_rotate(cpy, node, undo_dir_)
            self.assertTrue(BT.ABT_equals(cpy, self.trees[index]), f"_ABT_rotate reverse failed for case {case}\n{self.trees[index]} --> {cpy}")
            
    def test_ABT_split_rotate(self):
        cases = [(3, 0, BT.DIR_LEFT, [(5,), (0,), (2,), (1,), N, N, (6,), (3,), (4,)]),
                 (3, 0, BT.DIR_RIGHT, [(4,), (1,), (0,), (3,), N, N, (2,), N, N, N, N, N, N, (5,), (6,)]),
                 (6, 0, BT.DIR_LEFT, [(5,), (0,), (2,), (1,), (11,), N, (6,), (3,)])]
        for i, case in enumerate(cases):
            index, node, dir_, res = case
            cpy = self.trees[index].copy()
            BT._ABT_split_rotate(cpy, node, dir_)
            self.assertTrue(BT.ABT_equals(cpy, res), f"_ABT_split_rotate failed to rotate tree[{index}] around {node}: {cpy} != {res}")
        # TODO: include the "un-split rotate" operations
        
        """
    @classmethod
    def setUpClass(cls):
        cls.trees = [[(0,),    (1,)],
                     [(0,),    N, (2,)], 
                     [(0,),    (1,),(2,)], 
                     [(0,),    (1,),(2,),    (3,),(4,),(5,),(6,)],
                     [(0,),    (1,), N,    (3,),(4,)],
                     [(0,),    N, (2,),    N, N,(5,),(6,)], 
                     [(0,),    (1,), (2,),    (3,),N,(5,),(6,),    N, N, N, N, (11,)],
                     [(0,),    (1,), (2,),    (3,),(4,),N,N,    (7,),(8,),(9,),N,N,N,N,N,    (15,),(16,),N,N,N,N,N,N,N,N,N,N,N,N,N,N,    (31,)]]
        """
    def test_ABT_inorder_traversal(self):
        results = [[(1,),(0,)],
                   [(0,),(2,)],
                   [(1,),(0,),(2,)],
                   [(3,),(1,),(4,),(0,),(5,),(2,),(6,)],
                   [(3,),(1,),(4,),(0,)],
                   [(0,),(5,),(2,),(6,)],
                   [(3,),(1,),(0,),(11,),(5,),(2,),(6,)],
                   [(31,),(15,),(7,),(16,),(3,),(8,),(1,),(9,),(4,),(0,),(2,)]]
        
        def collect(tree, index, out):
            out.append(tree[index])
            return BT.TRAVERSE_GO
        
        for i, tree in enumerate(self.trees):
            result = results[i]
            arr = []
            BT.ABT_traverse(tree, collect, arr, traversal=BT.TRAVERSE_INORDER)
            self.assertListEqual(result, arr, f"inorder traversal of tree[{i}] failed: {result} != {arr}")
            
    def test_ABT_preorder_traversal(self):
        results = [[(0,),(1,)],
                   [(0,),(2,)],
                   [(0,),(1,),(2,)],
                   [(0,),(1,),(3,),(4,),(2,),(5,),(6,)],
                   [(0,),(1,),(3,),(4,)],
                   [(0,),(2,),(5,),(6,)],
                   [(0,),(1,),(3,),(2,),(5,),(11,),(6,)],
                   [(0,),(1,),(3,),(7,),(15,),(31,),(16,),(8,),(4,),(9,),(2,)]]
        
        def collect(tree, index, out):
            out.append(tree[index])
            return BT.TRAVERSE_GO
        
        for i, result in enumerate(results):
            tree = self.trees[i]
            arr = []
            BT.ABT_traverse(tree, collect, arr, traversal=BT.TRAVERSE_PREORDER)
            self.assertListEqual(result, arr, f"preorder traversal of tree[{i}] failed: {result} != {arr}")
            
    def test_ABT_postorder_traversal(self):
        results = [[(1,),(0,)],
                   [(2,),(0,)],
                   [(1,),(2,),(0,)],
                   [(3,),(4,),(1,),(5,),(6,),(2,),(0,)],
                   [(3,),(4,),(1,),(0,)],
                   [(5,),(6,),(2,),(0,)],
                   [(3,),(1,),(11,),(5,),(6,),(2,),(0,)],
                   [(31,),(15,),(16,),(7,),(8,),(3,),(9,),(4,),(1,),(2,),(0,)]]
        
        def collect(tree, index, out):
            out.append(tree[index])
            return BT.TRAVERSE_GO
        
        for i, result in enumerate(results):
            tree = self.trees[i]
            arr = []
            BT.ABT_traverse(tree, collect, arr, traversal=BT.TRAVERSE_POSTORDER)
            self.assertListEqual(result, arr, f"postorder traversal of tree[{i}] failed: {result} != {arr}")
            
    def test_ABT_levelorder_traversal(self):
        results = [[(0,),(1,)],
                   [(0,),(2,)],
                   [(0,),(1,),(2,)],
                   [(0,),(1,),(2,),(3,),(4,),(5,),(6,)],
                   [(0,),(1,),(3,),(4,)],
                   [(0,),(2,),(5,),(6,)],
                   [(0,),(1,),(2,),(3,),(5,),(6,),(11,)],
                   [(0,),(1,),(2,),(3,),(4,),(7,),(8,),(9,),(15,),(16,),(31,)]]
        
        def collect(tree, index, out):
            out.append(tree[index])
            return BT.TRAVERSE_GO
        
        for i, result in enumerate(results):
            tree = self.trees[i]
            arr = []
            BT.ABT_traverse(tree, collect, arr, traversal=BT.TRAVERSE_LEVELORDER)
            self.assertListEqual(result, arr, f"levelorder traversal of tree[{i}] failed: {result} != {arr}")
            
    def test_ABT_inorder_traversal_reverse(self):
        results = [[(0,),(1,)],
                   [(2,),(0,)],
                   [(2,),(0,),(1,)],
                   [(6,),(2,),(5,),(0,),(4,),(1,),(3,)],
                   [(0,),(4,),(1,),(3,)],
                   [(6,),(2,),(5,),(0,)],
                   [(6,),(2,),(5,),(11,),(0,),(1,),(3,)],
                   [(2,),(0,),(4,),(9,),(1,),(8,),(3,),(16,),(7,),(15,),(31,)]]
        
        def collect(tree, index, out):
            out.append(tree[index])
            return BT.TRAVERSE_GO
        
        for i, tree in enumerate(self.trees):
            result = results[i]
            arr = []
            BT.ABT_traverse(tree, collect, arr, traversal=BT.TRAVERSE_INORDER, reverse=True)
            self.assertListEqual(result, arr, f"inorder reverse traversal of tree[{i}] failed: {result} != {arr}")
            
    def test_ABT_preorder_traversal_reverse(self):
        results = [[(0,),(1,)],
                   [(0,),(2,)],
                   [(0,),(2,),(1,)],
                   [(0,),(2,),(6,),(5,),(1,),(4,),(3,)],
                   [(0,),(1,),(4,),(3,)],
                   [(0,),(2,),(6,),(5,)],
                   [(0,),(2,),(6,),(5,),(11,),(1,),(3,)],
                   [(0,),(2,),(1,),(4,),(9,),(3,),(8,),(7,),(16,),(15,),(31,)]]
        
        def collect(tree, index, out):
            out.append(tree[index])
            return BT.TRAVERSE_GO
        
        for i, result in enumerate(results):
            tree = self.trees[i]
            arr = []
            BT.ABT_traverse(tree, collect, arr, traversal=BT.TRAVERSE_PREORDER, reverse=True)
            self.assertListEqual(result, arr, f"preorder reverse traversal of tree[{i}] failed: {result} != {arr}")
        
    def test_ABT_postorder_traversal_reverse(self):
        results = [[(1,),(0,)],
                   [(2,),(0,)],
                   [(2,),(1,),(0,)],
                   [(6,),(5,),(2,),(4,),(3,),(1,),(0,)],
                   [(4,),(3,),(1,),(0,)],
                   [(6,),(5,),(2,),(0,)],
                   [(6,),(11,),(5,),(2,),(3,),(1,),(0,)],
                   [(2,),(9,),(4,),(8,),(16,),(31,),(15,),(7,),(3,),(1,),(0,)]]
        
        def collect(tree, index, out):
            out.append(tree[index])
            return BT.TRAVERSE_GO
        
        for i, result in enumerate(results):
            tree = self.trees[i]
            arr = []
            BT.ABT_traverse(tree, collect, arr, traversal=BT.TRAVERSE_POSTORDER, reverse=True)
            self.assertListEqual(result, arr, f"postorder reverse traversal of tree[{i}] failed: {result} != {arr}")
        
    def test_ABT_levelorder_traversal_reverse(self):
        results = [[(0,),(1,)],
                   [(0,),(2,)],
                   [(0,),(2,),(1,)],
                   [(0,),(2,),(1,),(6,),(5,),(4,),(3,)],
                   [(0,),(1,),(4,),(3,)],
                   [(0,),(2,),(6,),(5,)],
                   [(0,),(2,),(1,),(6,),(5,),(3,),(11,)],
                   [(0,),(2,),(1,),(4,),(3,),(9,),(8,),(7,),(16,),(15,),(31,)]]
        
        def collect(tree, index, out):
            out.append(tree[index])
            return BT.TRAVERSE_GO
        
        for i, result in enumerate(results):
            tree = self.trees[i]
            arr = []
            BT.ABT_traverse(tree, collect, arr, traversal=BT.TRAVERSE_LEVELORDER, reverse=True)
            self.assertListEqual(result, arr, f"levelorder reverse traversal of tree[{i}] failed: {result} != {arr}")