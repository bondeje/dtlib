# dtlib
A small package of basic data structures and algorithms

# trees
Do you love trees? I love trees; exploring their various implementations and algorithms. This is a submodule of some basic and some less basic (but not advanced) realizations of trees. All of them are currently binary, but that will change soon enough.

## Basic module layout and tree data type interface/construction details

### Public tree type interfaces: Class/Interface name (inheritance notes) [status]
Class diagram to be produced when more mature. For now, indentation indicates it inherits from the interface above it
- `Tree` (`abc.Collection`) [complete, in testing]
  - `BinaryTree` [complete, in testing]
    - `BinarySearchTree` (`abc.Sequence`, can be configured to be `abc.Set`-like) [complete, in testing]
      - `OrderStatisticTree` [complete, in testing]
        - `WeightBalancedTree` [complete, in testing]
    - `BinaryHeap` [complete, in testing]
      - `MinMaxHeap` [partial with `ARRAY_STORAGE` complete, in testing]
### Classes
There are generally at least two concrete classes for each of the interfaces named `Array[Interface]` and `Linked[Interface]`, e.g. `ArrayWeightBalancedTree` and `LinkedWeightBalancedTree`, based on the underlying storage (described below). The class object for the interface can (and should) be used for instantiation of the corresponding class; they are factories for the actual concrete classes. Specifically, if you want to create a `BinarySearchTree` with `ARRAY_STORAGE` rather than `LINKED_STORAGE`, use `tree = BinarySearchTree(*args, storage=ARRAY_STORAGE, **kwargs)`. You can also use `tree = ArrayBinarySearchTree(*args, **kwargs)` but the former is preferred. Each interface has a default storage based on what makes most sense for the geometry of the tree. Trees that are balanced or complete will tend to have `ARRAY_STORAGE` preferred/default since they can take advantage of memory savings and speed improvements based on cache locality for large trees. Other trees will generally default to `LINKED_STORAGE`.

Other classes (`has a` relationship to the interfaces and their subclasses, NOT `is a`):
- `TreeMap` (`Mapping`, `BinarySearchTree`-like) [in planning]
- `HeapTree` (`Sequence`, `BinaryHeap`-like and `BinarySearchTree`-like) [in planning, open to name suggestions...this is NOT a `treap`]
  - `MinMaxTree` (`Sequence`, `MinMaxHeap`-like and `BinarySearchTree`-like) [partial, in testing]

### Public API details
As can be seen above, the trees here are all derived from `Tree`, which is really just a simple interface for basic functionality and queries or modifications that we can expect to be available on all trees.

For all trees, arbitrary data can be stored in each "Node" of the `Tree`. For the purposes of many trees which need to order, select, or at least differentiate contents based on attribute or derived quantity, all `Tree`s will support the storage of a `key` callable such that `key(stored data)` results in derived data that satisfies some minimal ordering (meaning at least `>` or `<`). 

As an implementation note, all traversal implementations and iterators are implemented in an iterative manner, specifically no recursion, so that the impact of the key can be isolated. This means that for data that inherently is its own key and has ordering, `key=None` (default) has a performance improvement. That being said, if the data ordering is provided by an evaluated function on its internal representation, then the performance difference is likely superficial but still has the added benefit of less code copy-paste and slightly less memory consumption. For example, if the data are just strings, which have a lexicographic ordering, always use `key=None` but if the data are `(key, value)` pairs to implement a `TreeMap` using `BinarySearchTree`, `key=lambda x: x[0]` makes sense but probably does not make much of a difference over say using creating a `pair` class with `__slots__=['k','v']` and for example `def __lt__(self, other): return self.k < other.k`. The latter method probably produces cleaner, more maintainable code.

#### `Tree` interface functions
| required function | standard semantics |
|:----------------- |:------------------ |
| `__contains__` | check if a key is in the `Tree` structure |
| `__iter__` | iterate over the elements of the tree |
| `__len__` | see `size` |
| `add` | insert or add a value to the tree data structure; <br>generally does not specify where |
| `discard` | remove a value from the tree data structure; <br>do nothing if value not present |
| `remove` | remove a value from the tree data structure; <br>value must be present or exception is raised |
| `size` | get the number of elements in the tree |
| `traverse` | move element by element in a specified or prescribed order and possibly apply some function |
| `validate` | evaluates that all defining properties of the tree type are met |

Tree inherits abc.Collection, however, the semantics of the various abstract methods and mixin methods can vary significant based on type of Tree and even how it is configured. 

#### `BinaryTree` interface functions
A collection of plain data ordered only by relationships to 3 neighboring nodes (parent, left child, right child)

No required interface functions. The concrete binary tree classes merely provide baseline implementations for subclasses. Though the direct subclasses of `BinaryTree` can be instantiated, there are not many uses cases for their instances.

##### A quick note about traversals
The `BinaryTree`s provide the base implementations of `traverse` for all `BinaryTree` subclasses. Traversal orders are specified by one of 4 flags, which are defined in `dtlib.trees._constants`. They are as below
| traversal flag | visit order |
|:-------------- |:----------- |
| `TRAVERSE_INORDER` | left child, node, right child |
| `TRAVERSE_PREORDER` | node, left child, right child |
| `TRAVERSE_POSTORDER` | left child, right child, node |
| `TRAVERSE_LEVELORDER` | left to right for nodes on the same level from root of tree to leaves |

Traversals can be done in two ways:
1) procedural traversals where a function and its arguments and keywords are passed to the traversing function and applied to every node as it is visited along the traversal
   - this method, though somewhat tedious requiring a function following a specification for each application, is quite general
   - user has control over termination of the traversal with the flags `TRAVERSE_GO` and `TRAVERSE_STOP`
   - use `tree.traverse(*args, **kwargs)`
2) iterators for simple interfaces to the many python interfaces that accept iterables
   - use `tree.__iter__()`, `tree.__reversed__()` for configured default traversals and `tree.iterator(*args, **kwargs)` to configure the traversal on the fly.

#### `BinarySearchTree` interface functions
Data in a `BinaryTree` organized for searching and sorting optimization.
| required function | standard semantics |
|:----------------- |:------------------ |
| `__getitem__` | provide the value at the provided rank statistic; `a[k]` provides the data that have `k` keys before it in an inorder traversal |
| `__iter__` | create an iterator; default behavior is to iterate in `inorder` traversal |
| `__reversed__` | create a reversed iterator; default behavior is to iterate in reverse `inorder` traversal |
| `index` | provide the selection statistic for that matches the provided key; `a[a.index(value)] = value` |
| `count` | number of instances found that matches the key |
| `search` | find an element that matches the key |

General implementation notes: 
- can be configured to allow duplicate keys (default) or not to allow more `set`-like behavior
- insertion order is stable, i.e. the sort resulting from a sequence of insertions followed by inorder traversal is a stable sort
- reverse is done in O(1) time with an internal handle by using the member function `reverse()`, which is also compatible with `__reversed__` iteration. It is highly suggested not to reverse by defining a `key` that reverses a natural ordering if you do not have to. Specifically `a=BinarySearchTree(iterable, reverse=True)` for elements that already obey an ordering rather than something like `a=BinarySearchTree(iterable, key=lambda x: -x)` like you might do to make a `heapq` heap a "max heap". 
- in the case of duplicates, search can be configured to find the first inserted, first encountered (default), or last inserted key with the flags `SEARCH_FIRST_INORDER`, `SEARCH_FIRST_LEVELORDER`, and `SEARCH_LAST_INORDER`, respectively.

#### `OrderStatisticsTree` interface functions
Data in a `BinarySearchTree` for which rank and selection query are optimized
| required function | standard semantics |
|:----------------- |:------------------ |
| `select` | find the kth element in order |
| `rank`   | find the sequence index corresponding to a key |

#### `WeightBalancedTree` interface functions
Data in an `OrderStatisticTree` with optimization on the tree structure (self-balancing) to improve query times and, for `Array` storage, memory

No required interface functions.

#### `BinaryHeap` interface functions
A traditional Min- or Max- heap, configurable by the User
| required function | standard semantics |
|:----------------- |:------------------ |
| `maximum` | access the value with the maximum key in the system |
| `minimum` | access the value with the minimum key in the heap |
| `peek` | access the root node of the heap |
| `pop` | remove and return the root node of the heap |
| `push` | add a new value to heap |
| `pushpop` | simultaneous push and pop |

#### `MinMaxHeap` interface functions
A dually embedded Heap structure optimized for both `min` and `max` queries at the same time
| required function | standard semantics |
|:----------------- |:------------------ |
| `pop_max` | remove and return the value with the maximum key |
| `pop_min` | remove and return the value with the minimum key |
| `pushpop_max` | simultaneous pusha and remove and return the value with the maximum key |
| `pushpop_min` | simultaneous push and remove and return the value with the minimum key |

### Algorithm performance table

Big O notation for expected or amortized cases (in the case of dynamic structures). When two values are shown as it O(log n)-O(n), the 1st is for the `ARRAY_STORAGE` while the 2nd is for the `LINKED_STORAGE` versions. When two values in the O notation are separated by '->', the right one is the worst-case scenario, i.e. O(log n -> n) for binary search

```
n = number of elements
m = number of copies of data, assuming copies are allowed
k = order statistic
```

Computational
| Algorithm \ `Tree` -> | `BinaryTree` | `BinarySearchTree` | `OrderStatisticTree` | `WeightBalancedTree` | (Min)`Heap`    | (Max)`Heap`    | `MinMaxHeap`    | `MinMaxTree`<br> (with WBT) |
|:---------------------:|:------------:|:------------------:|:--------------------:|:--------------------:|:--------------:|:--------------:|:---------------:|:----------:|
| `__contains__`        | O(n)         | O(log n -> n)      | O(log n -> n)        | O(log n)             | O(n)           | O(n)           | O(n)            | O(log n)   |
| `count`               | O(n)         | O(log n -> n)      | O(log n -> n)        | O(log n)             | O(n)           | O(n)           | O(n)            | O(log n)   |
| `size`/`__len__`      | O(n)         | O(n)               | O(1)                 | O(1)                 | O(1)-<br>O(log n)^1 | O(1)-<br>O(log n)^1 | O(1)-<br>O(log n)^1  | O(1)       |
| `add`                 | O(1)-O(n)    | O(log n -> n)      | O(log n -> n)        | O(log n -> n)-<br>O(log n)             | O(log n)       | O(log n)       | O(log n)        | O(log n)   |
| `remove`/`discard`    | O(n)         | O(log n -> n)      | O(log n -> n)        | O(log n)             | O(log n)       | O(log n)       | O(log n)        | O(log n)   |
| `search`              | O(n)         | O(log n -> n)      | O(log n -> n)        | O(log n)             | O(n)           | O(n)           | O(n)            | O(log n)   |
| `minimum`             | O(n)         | O(log n -> n)      | O(log n -> n)        | O(log n)             | O(1)           | O(n)           | O(1)            | O(1)       |
| `maximum`             | O(n)         | O(log n -> n)      | O(log n -> n)        | O(log n)             | O(n)           | O(1)           | O(1)            | O(1)       |
| `select`              | O(n)         | O(log n -> n)      | O(log n -> n)        | O(log n)             | O(n)           | O(n)           | O(n)            | O(log n)   |
| `rank`                | O(n)         | O(log n -> n)      | O(log n -> n)^2      | O(log n)^2           | O(n)           | O(n)           | O(n)            | O(log n)   |
| `pop`                 | N/A          | N/A                | N/A                  | N/A                  | O(log n)       | O(log n)       | O(log n)        | O(log n)   |
| `push`                | N/A          | N/A                | N/A                  | N/A                  | O(log n)       | O(log n)       | O(log n)        | O(log n)   |

^1 not fully implemented

^2 `rank` complexity includes `search` in the general case, but `search` and determination of `rank` once the internal node is found are both O(log n). For OrderStatisticTree and subclasses, the overhead for determining the `rank` after the internal node is found is only O(1).


### Internal details
A separate metaclass `TreeMeta` exists to customize construction of `Tree` subclasses, interfaces. For now, all this metaclass does is account for the ability to specify the storage paradigms. For all implemented `Trees`, I endeavor to make at least 2 storage paradigms available. More may be made in the future to further optimize performance.

#### Storage paradigms
| Paradigm | Description | Advantages | Disadvantages |
|:-------- |:----------- |:---------- |:------------- |
| Array | The tree is stored as a sequence of nodes in a list | pointer/reference data locality for fast read/write access. <br> navigation algorithms are simple as fewer pointer stores need to be updated | poorly balanced trees or frequent, large data rearrangements may offset locality advantages |
| Linked | The tree is stored as linked node objects; the "traditional" storage of trees. | modifications algorithms are very simple | requires additional pointer memory to link nodes that need to be maintained <br> large datasets will suffer pointer non-locality performance losses |
   
Each storage paradigm has its own class hierarchy for each tree type defined in separate `.py` files to organize the functionality attributable to the classes and types. For example, there are a `_LinkedBinarySearchTree.py` and a `_ArrayBinarySearchTree.py` that define the algorithms associated with the classes `LinkedBinarySearchTree` and `ArrayBinarySearchTree`, which are defined in the interface file `BinarySearchTree.py`. The tree type has one set of inheritances through concrete classes while the interface type has a separate hierarchy. In the same example, `LinkedBinarySearchTree` both inherits from `LinkedBinaryTree`, which defines the functionality of a binary tree with a `Linked` storage paradigm and the `BinarySearchTree` interface class, which acts more as both an interface and an instance factory of classes that inherit the interface than a true multiple inheritance. `BinarySearchTree`, which itself inherits from `BinaryTree`, cannot be instantiated (and nor can `BinaryTree`). This is done in part to separate to the public API from the internal API so that it is easier to maintain abstraction while freely allowing updates. In particular, all the functionality in the files beginning with "\_" could be translated to the python C api for performance boosts while the public API defining files would remain largely unchanged. In fact, this is the intention, which I hope is clear by seeing that the function signatures are all in or close to C-style.

#### Nodes

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

#### Node storage
| Node type^1 | description | valid attributes | Advantages | Disadvantages |
|:----------- |:----------- |:---------------- |:---------- |:------------- |
| `LIST_NODE` | a simple list for node decorations with integer indices as attributes^2 | non-negative integer indices| fast, small overhead | no flexibility on attributes and high maintenance, sketchy typing at best |
| `DICT_NODE` | store node as a dictionary with keys as attributes | hashable values | flexibility in attributes, low memory overhead, fast if attributes are simple | slightly less sketchy typing than `LIST_NODE` | indirect typing |
| `CLASS_NODE` | store node as a class instance with attributes | hashable values | most flexible in attributes, clear typing | largest memory overhead, probably slightly slower than `DICT_NODE` |
| `SLOTTED_CLASS_NODE` | store node attributes in class with `__slots__`^3 | string identifiers, specifically cannot be numerical strings | low memory overhead, fast | limited flexibility on attributes |

^1 in all node types, `VALUE_KEY` is a required attribute that should not be changed or overwritten.

^2 for `LIST_NODE`, a warning that augmented attributes should be sequential integers. If not sequential, there is additional memory overhead. Which sequential values are available depends on the storage mechanisms and required attributes of the particular Tree type. For this reason, `LIST_NODE` is good for defaults, but if you need to augment, you should be using at the very least `DICT_NODE`.

^3 for `SLOTTED_CLASS_NODE`, it is still possible to accidentally inherit from a `CLASS_NODE` without error, which would destroy all the advantages of a `SLOTTED_CLASS_NODE`. Tread carefully and always test to ensure that the `__dict__` attribute is not present when creating a new node class.

Nodes do not all have unique types, but there is some ability to have typing capability if the developer wants to create an extensions that passes nodes between different tree types. Applying types to `LIST_NODE` instances would require more strict control of the attributes of the nodes. In principle, one could just reserve each index for a particular preset decoration and then type would merely be the size of the list. Applying types to `DICT_NODE` could be achieved by `a.keys() <= b.keys()` meaning "`a` is a `b`" for two `DICT_NODE`s `a` and `b`. This would require that no key can have a different semantic meaning. Currently for `LIST_NODE` and `DICT_NODE`, the constant `SIZE_KEY` violates these requirements as it both has different values depending on the storage and interferes with `PARENT_KEY` in the `LinkedOrderStatistics` and `LinkedBinaryHeap` types. This was done to minimize the memory overhead in the `LIST_NODE` node storage for these types as compared to the `ARRAY_STORAGE`.

For `CLASS_NODE` and `SLOTTED_CLASS_NODE`, there are already built-in typing capability that more or less matches that which is described above for `DICT_NODE`, but there is an explicit mechanism and instance testing

```
from dtlib.trees._BinaryNode import Node_factory
from dtlib.trees._constants import VALUE_KEY, DIR_LEFT, DIR_RIGHT, CLASS_NODE

ClassNode = Node_factory(CLASS_NODE) # creates a node class with a default naming scheme with attribute VALUE_KEY and default None
# note: if name is not provided, there is internal machinery to provide a unique name that is tracked, but this naming will not be related to the output of ClassNode_factory
a = ClassNode(0)  # a is an instance of ClassNode
a[VALUE_KEY]      # = 0

SubClassNode = Node_factory(CLASS_NODE, {DIR_LEFT: None}, parent=ClassNode) # creates a node class with a default naming scheme with attributes [VALUE_KEY, DIR_LEFT] defaulted to None
b = SubClassNode(-1, 1)   # b is an instance of SubClassNode
b[VALUE_KEY]              # = -1
b[DIR_LEFT]               # = 1
isinstance(b, ClassNode)  # = True

SubSubClassNode = Node_factory(CLASS_NODE, {DIR_RIGHT: None}, parent=SubClassNode) # creates a node class with a default naming scheme with attributes [VALUE_KEY, DIR_LEFT, DIR_RIGHT] defaulted to None
#c = SubSubClassNode(-1, 1, 2)    # c is an instance of SubClassNode
c[VALUE_KEY]                  # = -1
c[DIR_LEFT]                   # = 1
c[DIR_RIGHT]                  # = 2
isinstance(c, ClassNode)      # = True
isinstance(c, SubClassNode)   # = True
```

In principle, the same thing can be done with `DICT_NODE` by subclassing `dict` on the fly, but this will require creating a standard class inheriting from `dict` which kind of defeats the purpose of having a pure `dict` type node. In this case, just use `CLASS_NODE` or if you want to be more efficient about attributes and instance sizes, use `SLOTTED_CLASS_NODE`.

## Types of trees planned (numbers not necessarily indicating order of priority)
1) AVL tree
2) Red-Black tree
3) Segment tree
   - 1D
   - 2D/nD
4) Interval tree
5) Binary Indexed Tree
6) B-tree (a generalization of but not necessarily encapsulating Binary Trees to keep the Binary Tree implementations as light and clear as possible)
7) Binomial Heap
8) Pairing Heap
9) Fibonacci Heap
10) Treap
11) SplayTree
