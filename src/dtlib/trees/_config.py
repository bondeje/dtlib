LIST_NODE = 'l'
DICT_NODE = 'd'
CLASS_NODE = 'c'
SLOTTED_CLASS_NODE = 'cs'

tree_params = {"TreeNode": LIST_NODE}

def configure(**kwargs):
    for k, v in kwargs.items():
        tree_params[k] = v
        print(f"updated tree_params[{k}] = {v}")