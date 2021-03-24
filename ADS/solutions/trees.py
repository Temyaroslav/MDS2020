import math

class Node:
    def __init__(self, key=0, parent=None):
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent

def insert(root, node):
    if root.key > node.key:
        if root.left is None:
            root.left = node
            node.parent = root
        else:
            insert(root.left, node)
    else:
        if root.right is None:
            root.right = node
            node.parent = root
        else:
            insert(root.right, node)

#######################################################

def tree_size(root):
    if root is None:
        return 0
    return 1 + tree_size(root.left) + tree_size(root.right)

def tree_max(root):
    if root is None:
        return -math.inf
    return max(root.key, tree_max(root.left), tree_max(root.right))

def tree_min(root):
    if root is None:
        return math.inf
    return min(root.key, tree_min(root.left), tree_min(root.right))

def _check_BST(root):
    """
    An auxuliary recursive function for check_BST
    Input: root - a root node of a binary tree (may be None)
    Output: a tuple consisting of
        1. True if the tree is BST, False otherwise
        2. the smallest key in the tree
        3. the largest key in the tree
    """
    if root is None:
        return (True, math.inf, -math.inf)
    left_BST, left_min, left_max = _check_BST(root.left)
    right_BST, right_min, right_max = _check_BST(root.right)
    global_min = min(root.key, left_min, right_min)
    global_max = max(root.key, left_max, right_max)
    if left_BST and right_BST and (left_max <= root.key <= right_min):
        return (True, global_min, global_max)
    return (False, global_min, global_max)

def check_BST(root):
    return _check_BST(root)[0]

def _min_diff(root):
    """
    An auxiliary recursive function for min_diff
    Input: root - a root node of a binary tree (may be None)
    Output: a tuple consisting of
        1. the minimum absolute value of two keys in the tree
        2. the smallest key
        3. the largest key
    """
    if root is None:
        return (math.inf, math.inf, -math.inf)
    left_min_diff, left_min, left_max = _min_diff(root.left)
    right_min_diff, right_min, right_max = _min_diff(root.right)
    return (
        min(left_min_diff, right_min_diff, root.key - left_max, right_min - root.key),
        min(left_min, root.key),
        max(right_max, root.key)
    )

def min_diff(root):
    return _min_diff(root)[0]

#################################################

if __name__ == "__main__":
    T = Node(3)
    insert(T, Node(1))
    insert(T, Node(2))
    print(check_BST(T))