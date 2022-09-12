# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 09:07:52 2022

@author: jeffr
"""

from dtlib.trees._constants import DIR_LEFT, DIR_RIGHT, VALUE_KEY, \
    LIST_NODE, DICT_NODE, CLASS_NODE, SLOTTED_CLASS_NODE

# for when node_factory is compatible with ArrayBinary*Tree
# there is maintenance and porting value to having cases where there is a node simply just to store VALUE_KEY
# while only adding memory to the most basic of trees: BinaryTree when storage is Array: standard BSTs, Heaps, MinMaxHeaps, etc.
# this also makes the translation to C/C++ more clear as we can just swap None-->Null (C), --> nullptr (C++)
def ListNode_factory(specs=None, /):
    if specs is None:
        specs = {}
    _specs = [(VALUE_KEY, None)]
    _specs.extend(specs.items())
    def list_node_factory(*args):
        Nargs = len(args)
        return [args[i] if i < Nargs else _spec[1] for i, _spec in enumerate(_specs)]
    return list_node_factory    

def DictNode_factory(specs=None, /):
    if specs is None:
        specs = {}
    _specs = [(VALUE_KEY, None)]
    _specs.extend(specs.items())
    def dict_node_factory(*args):
        Nargs = len(args)
        return {_spec[0]: (args[i] if i < Nargs else _spec[1]) for i, _spec in enumerate(_specs)}
    return dict_node_factory

class ClassNode:
    def __getitem__(self, key):
        return self.__dict__[key]
    def __setitem__(self, key, value):
        self.__dict__[key] = value
    def __str__(self):
        return str(self[VALUE_KEY])
    
def ClassNode_subclass_init(obj_self, *args):
    Narg = len(args)
    for i, _spec in enumerate(obj_self._specs):
        obj_self.__dict__[_spec[0]] = args[i] if i < Narg else _spec[1]
        
_next_class_node_subclass = 'ClassNode_0'
ClassNode_subclasses = {}

def _get_next_class_node_subclass():
    global _next_class_node_subclass
    out = _next_class_node_subclass
    _next_class_node_subclass = 'ClassNode_' + str(int(_next_class_node_subclass.split('_')[-1]) + 1)
    return out

def ClassNode_factory(specs=None, name=None, /):
    if specs is None:
        specs = {}
    _specs = [(VALUE_KEY, None),]
    if name is None or name in ClassNode_subclasses:
        if name in ClassNode_subclasses:
            raise Warning(f"attempting to create a named subclass {name} of ClassNode that already exists")
        name = _get_next_class_node_subclass()
    _specs.extend(specs.items())
    obj = type(name, (ClassNode, ), {'_specs': _specs, '__init__': ClassNode_subclass_init})
    return obj

class SlottedClassNode:
    __slots__ = []
    def __getitem__(self, key):
        return getattr(self, self._slot_keys[key])
    def __setitem__(self, key, value):
        setattr(self, self._slot_keys[key], value)
    def __str__(self):
        return str(self[VALUE_KEY])
    
def SlottedClassNode_subclass_init(obj_self, *args):
    Narg = len(args)
    for i, _spec in enumerate(obj_self._specs):
        obj_self.__setitem__(_spec[0], args[i] if i < Narg else _spec[1])
        
_next_slotted_class_node_subclass = 'SlottedClassNode_0'
SlottedClassNode_subclasses = {}

def _get_next_slotted_class_node_subclass():
    global _next_slotted_class_node_subclass
    out = _next_slotted_class_node_subclass
    _next_slotted_class_node_subclass = 'SlottedClassNode_' + str(int(_next_slotted_class_node_subclass) + 1)
    return out

def SlottedClassNode_factory(specs=None, name=None, /):
    if specs is None:
        specs = {}
    _specs = [(VALUE_KEY, None)]
    if name is None or name in ClassNode_subclasses:
        if name in ClassNode_subclasses:
            raise Warning(f"attempting to create a named subclass {name} of ClassNode that already exists")
        name = _get_next_class_node_subclass()
    _specs.extend(specs.items())
    _slots = ['_' + str(_spec[0]) for _spec in _specs]
    _slot_map = {_specs[i][0]: _slots[i] for i in range(len(_specs))}
    obj = type(name, (SlottedClassNode, ), {'_slot_keys': _slot_map, '_specs': _specs, '__slots__': _slots, '__init__': SlottedClassNode_subclass_init})
    
    return obj

# returns the appropriate node factory for the requested storage mode
# if **kwargs is not empty, specifies the spec of the 
def Node_factory(storage=LIST_NODE, specs=None, name=None, /):
    if storage == LIST_NODE:
        return ListNode_factory(specs)
    elif storage == DICT_NODE:
        return DictNode_factory(specs)
    elif storage == CLASS_NODE:
        return ClassNode_factory(specs, name)
    elif storage == SLOTTED_CLASS_NODE:
        return SlottedClassNode_factory(specs, name)
    else:
        raise ValueError(f"unknown storage mechanism {storage} for Binary Tree nodes")