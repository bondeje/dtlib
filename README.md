# dtlib
A small package of basic data structures and algorithms

## trees
Do you love trees? I love trees; exploring their various implementations and algorithms. This is a submodule of some basic and some less basic (but not advanced) realizations of trees. All of them are currently binary, but that will change soon enough.

### Basic module layout and tree data type interface/construction details

Tree types 

##### Public tree types (class diagram to be produced when more mature)
- Tree
  - BinaryTree - A collection of plain data ordered only by manual relationships to neighboring data
    - BinarySearchTree - Data in a Binary Tree organized for searching and sorting optimization
      - OrderStatisticsTree - Data in a Binary Search Tree for which rank and selection query optimization
        - WeightBalancedTree - Data in an OrderStatisticTree with optimization on the tree structure (self-balancing) to improve query times and, for `Array` storage, memory
    - BinaryHeap - A traditional Min- or Max- heap, configurable by the User
      - MinMaxHeap - A dually embedded Heap structure optimized for both `min` and `max` queries at the same time
     
#### Public API details
As can be seen above, the trees here are all derived from `Tree`, which is really just a simple interface for basic functionality and queries or modifications that we can expect to be available on all trees. 

###### Tree interface functions (subject to change)
| required function | standard semantics | exceptions |
|:----------------- |:------------------ |:---------- |
| `size` | get the number of elements in the tree | N/A |
| `__len__` | same as `size` | N/A |
| `add` | insert or add a value to the tree data structure; <br>generally does not specify where | heaps currently do not support, use `push` |
| `remove` | remove a value from the tree data structure; <br>value must be present or exception is raised | heaps currently do not support, use `pop`, <br> which does not raise exception |
| `discard` | remove a value from the tree data structure; <br>do nothing if not present | heaps currently do not support, use `pop` |

This does not mean all implementations of these functions have the same semantics nor that all trees implement them with the same interface. For some trees, usually those with opaque structures, the normal semantics of the function is different enough that the function is blocked until a clear use case is defined. For example, a heap usually only cares about removal of the head/root of the underlying tree. The heap implementations has a specific function to do this, `pop`, but the `remove` function is not defined/not implemented since `removal` of an arbitrary value in a heap does not have a clear use case and definitely cannot use the same one as a plain `Binary Tree` from which it would otherwise inherit `removal`. It might be defined as an alias in the future for the heap-specific functions, but definitely not have the semantics of `remove` as say used by any of the `Binary Search Trees`.

#### Internal details
A separate metaclass `TreeMeta` exists to customize construction of `Tree` subclasses, interfaces. For now, all this metaclass does is account for the ability to specify the storage paradigms. For all implemented `Trees`, I endeavor to make at least 2 storage paradigms available. More may be made in the future to further optimize performance.

##### Storage paradigms
| Paradigm | Description | Advantages | Disadvantages |
|:-------- |:----------- |:---------- |:------------- |
| Array | The tree is stored as a sequence of nodes in a list | pointer/reference data locality for fast read/write access. <br> navigation algorithms are simple as fewer pointer stores need to be updated | poorly balanced trees or frequent, large data rearrangements may offset locality advantages |
| Linked | The tree is stored as linked node objects; the "traditional" storage of trees. | modifications algorithms are very simple | requires additional pointer memory to link nodes that need to be maintained <br> large datasets will suffer pointer non-locality performance losses |
   
Each storage paradigm has its own class hierarchy for each tree type defined in separate `.py` files to organize the functionality attributable to the classes and types. For example, there are a `_LinkedBinarySearchTree.py` and a `_ArrayBinarySearchTree.py` that define the algorithms associated with the classes `LinkedBinarySearchTree` and `ArrayBinarySearchTree`, which are defined in the interface file `BinarySearchTree.py`. The tree type has one set of inheritances through concrete classes while the interface type has a separate hierarchy. In the same example, `LinkedBinarySearchTree` both inherits from `LinkedBinaryTree`, which defines the functionality of a binary tree with a `Linked` storage paradigm and the `BinarySearchTree` interface class, which acts more as both an interface and an instance factory of classes that inherit the interface than a true multiple inheritance. `BinarySearchTree`, which itself inherits from `BinaryTree`, cannot be instantiated (and nor can `BinaryTree`). This is done in part to separate to the public API from the internal API so that it is easier to maintain abstraction while freely allowing updates. In particular, all the functionality in the files beginning with '_' could be translated to the python C api for performance boosts while the public API defining files would remain largely unchanged. In fact, this is the intention, which I hope is clear by seeing that the function signatures are all in or close to C-style.

All trees contain node structures, even those following the Array storage paradigms. This means there is at minimum pointer cost overhead for memory compared to the most memory efficient implementations. The reason this is done to maximize cross compatibility of abstractions through interface consistency. For example, whereas the `heapq` module can do heaps "inplace" on the raw data in a sequence without having an intermediate node structure, an `OrderStatisticsTree`, which requires storage of a size/weight "decoration" in each element, either would require an intermediate node structure or forces the user to develop and maintain values that have the required decorations. The decorations would have to conform to the implementation specific methods for access or algorithms/factories would have to be developed to account for each of the different organizations of the values and decorations. This tedium can be ignored completely by requiring nodes and reserving attributes for the required decorations while the values are arbitrarily extensible. The latter strategy has been chosen, which, for the moment, requires additional pointer memory for all trees even in trivial data type cases.

That being said, there are currently 4 base configurations for nodes that each have extensible factories for defining augmentations. They are listed in the table below. To augment a node, one merely has to use the `Node_factory` that is available in `dtlib.trees._BinaryNode` with the interface defined below

```
node_factory = Node_factory(node_type, specs_dictionary)
  Arguments:
    - node_type - any of the reserved identifiers from the list of "node type" below
    - specs_dictionary - a dict with keys as attribute names and values as the defaults when creating new nodes. Note that the attribute VALUE_KEY, being required by all trees/nodes, does not need to be specified.
  Returns:
    - node_factory - a function which takes a single element and allocates a node with that value
```

Ex. a node for an OrderStatisticsTree that contains, data, a pointer to its parent, leftchild, rightchild, next inorder node can be created as follows

```
inorder_linked_node = Node_factory(DICT_NODE, {LEFT_CHILD: None, RIGHT_CHILD: None, SIZE_KEY: 1, "parent": None, "next": None})
```

Note: LEFT_CHILD, RIGHT_CHILD, SIZE_KEY being common decorations of nodes, have predefined values that can be used. They can be overridden as well, but care must be taken as there are no guarantees yet that inherited functionality will work if these values are changed.

to create a new node is then
```
nodeA = inorder_linked_node(dataA)
nodeA[LEFT_CHILD] = inorder_linked_node(dataB)
nodeA[LEFT_CHILD]["parent"] = nodeA
nodeA[SIZE_KEY] += 1

nodeA[VALUE_KEY] # = dataA
nodeA[SIZE_KEY] # = 2
nodeA[LEFT_CHILD] # = <node with dataB>
nodeA[LEFT_CHILD][VALUE_KEY] # = dataB
nodeA[LEFT_CHILD]["parent"][VALUE_KEY] # = dataA
nodeA[RIGHT_CHILD] # = None
nodeA["parent"] # = None
nodeA["next"] # = None
```

##### Node storage
| Node type^1 | description | identifier |
|:--------- |:------------ |:---------- |
| LIST_NODE | a simple list for node decorations with integer indices as attributes^2 | non-negative integer indices|
| DICT_NODE | store node as a dictionary with keys as attributes | hashable values |
| CLASS_NODE | store node as a class instance with attributes | hashable values |
| SLOTTED_CLASS_NODE | store node attributes in class with `__slots__` | string identifiers, specifically cannot be numerical strings |

^1 in all node types, `VALUE_KEY` is a required attribute that should not be changed or overwritten.

^2 for LIST_NODE, a warning that augmented attributes should be sequential integers. If not sequential, there is additional memory overhead. Which sequential values are available depends on the storage mechanisms and required attributes of the particular Tree type. For this reason, LIST_NODE is good for defaults, but if you need to augment, you should be using at the very least DICT_NODE.

### Types of trees planned (numbers not necessarily indicator order of priority)
1) AVL tree
2) Red-Black tree
3) Segment tree
   - 1D
   - 2D/nD
4) Interval tree
5) Binary Indexed Tree
6) B-tree (a generalization of but not necessarily encapsulating Binary Trees to keep the Binary Trees implementations as light and clear as possible)
7) Binomial Heap
8) Pairing Heap
9) Fibonacci Heap
