# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 18:26:32 2022

@author: jeffr
"""

# given a posive integer 0 < int_, calculate next higher power of 2
def _next_pow2(int_):
    return 1 << ((int_).bit_length())

# given an integer 0 <= int_, calculate next higher multiple of 2
def _next_mult2(int_):
    return ((int_+1) >> 1) << 1

# for given positive integers 0 <= start <= end, calculates the index in the middle; useful for binary trees in array format and binary searches/bisect (hence name root)
def _interval_root(start, end):
    return start + ((end-start) >> 1)