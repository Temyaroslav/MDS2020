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


def tree_size(root: Node):
    if root is None:
        return 0
    return 1 + tree_size(root.left) + tree_size(root.right)


def count_distinct(root: Node):
    return len(_count_distinct(root, set()))


def _count_distinct(root: Node, keys: set):
    if root is None:
        return keys

    res_left = _count_distinct(root.left, keys)
    res_right = _count_distinct(root.right, keys)

    return res_left | res_right | {root.key}


def tree_max(root: Node):
    return max(root.key,
               tree_max(root.left) if root.left else -math.inf,
               tree_max(root.right) if root.right else -math.inf)


def _check_BST(root: Node, mini, maxi):
    if root is None:
        return True
    if root.key < mini or root.key > maxi:
        return False

    res_left = _check_BST(root.left, mini, root.key - 1)
    res_right = _check_BST(root.right, root.key, maxi)

    return res_left and res_right


def check_BST(root):
    return _check_BST(root, -math.inf, math.inf)


def _min_diff(root: Node, mini=math.inf):
    if root is None:
        return mini
    if root.left is not None:
        mini = min(mini, root.key - root.left.key)
    if root.right is not None:
        mini = min(mini, root.right.key - root.key)
    res_left = _min_diff(root.left, mini)
    res_right = _min_diff(root.right, mini)
    return min(res_left, res_right)


def min_diff(root):
    return _min_diff(root)

#################################################


if __name__ == "__main__":
    # T = Node(5)
    # insert(T, Node(6))
    # insert(T, Node(2))
    T = Node(7)
    insert(T, Node(6))
    insert(T, Node(8))
    insert(T, Node(7))
    # print(tree_max(T))
    # should print True
    # print(check_BST(T))
    # should print 1
    # print(min_diff(T))
    print(count_distinct(T))