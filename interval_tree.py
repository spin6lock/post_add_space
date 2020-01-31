#!/usr/bin/env python3
#encoding:utf8
"""
This module provide interface to build a interval
tree. Also with the search API to decide whether
an interval is inside.
"""

import random

class TreeNode():
    """ node structure of the tree """
    def __init__(self, low, high):
        self.low = low
        self.high = high
        self.left = None
        self.right = None
        self.max = high
        self.height = 1

    def __str__(self):
        return "[{low},{high}], max:{max}".format(max=self.max, low=self.low, high=self.high)

    def to_interval(self):
        return (self.low, self.high)

def left_rotate(child, parent):
    left_child = child.left
    child.left = parent
    parent.right = left_child
    parent.height = calc_height(parent)
    return child

def right_rotate(child, parent):
    right_child = child.right
    parent.left = right_child
    child.right = parent
    parent.height = calc_height(parent)
    return child

def rebalance(node):
    left_height = get_height(node.left)
    right_height = get_height(node.right)
    if left_height - right_height > 1: # left case
        left_child = node.left
        left_grandchild_height = get_height(left_child.left)
        right_grandchild_height = get_height(left_child.right)
        if left_grandchild_height - right_grandchild_height > 0: # left left case
            node = right_rotate(left_child, node)
        else: # left right case
            left_child = left_rotate(left_child.right, left_child)
            node = right_rotate(left_child, node)
    elif right_height - left_height > 1: # right case
        right_child = node.right
        left_grandchild_height = get_height(right_child.left)
        right_grandchild_height = get_height(right_child.right)
        if left_grandchild_height - right_grandchild_height > 0:
            right_child = right_rotate(right_child.left, right_child)
            node = left_rotate(right_child, node)
        else:
            node = left_rotate(right_child, node)
    return node

def get_height(node):
    if not node:
        return 0
    return node.height

def calc_height(node):
    left_height = get_height(node.left)
    right_height = get_height(node.right)
    return max(left_height, right_height) + 1

def recursive_calc_max(node):
    if not node:
        return None
    left_max = recursive_calc_max(node.left)
    right_max = recursive_calc_max(node.right)
    lst = [left_max, right_max, node.max]
    node.max = max([i for i in lst if i is not None])
    return node.max

def insert_node(node, new):
    """
    insert to the correct place
    update max value as well
    """
    if not node:
        return new
    if new.low < node.low:
        node.left = insert_node(node.left, new)
    else:
        node.right = insert_node(node.right, new)
    node = rebalance(node)
    node.height = calc_height(node)
    return node

def pprint_tree(node, file=None, _prefix="", _last=True):
    print(_prefix, "`- " if _last else "|- ", str(node), sep="", file=file)
    if not node:
        return
    if not node.left and not node.right:
        return
    _prefix += "   " if _last else "|  "
    print("right:", end="")
    pprint_tree(node.right, file, _prefix, False)
    print("left: ", end="")
    pprint_tree(node.left, file, _prefix, True)

def build_tree(intervals):
    """
    Initialize interval tree

    Build the whole tree with TreeNode type.

    Parameters:
    intervals(list): list of intervals, intervals is
    tuple like (15, 20), both included.

    Returns:
    Root Node of the tree.
    """
    assert len(intervals) > 0
    root = None
    for interval in intervals:
        assert interval[0] <= interval[1]
        new = TreeNode(interval[0], interval[1])
        new.max = new.high
        root = insert_node(root, new)
    recursive_calc_max(root)
    return root

def check_tree(root_node):
    assert root_node
    if root_node.left:
        left_node = root_node.left
        assert left_node.low <= root_node.low
        assert left_node.max <= root_node.max
        check_tree(left_node)
    if root_node.right:
        right_node = root_node.right
        assert right_node.low >= root_node.low
        assert right_node.max <= root_node.max
        check_tree(right_node)

def search_tree(root_node, x):
    """
    search x in tree root by root_node

    if root_node is None, return
    if x in root_node interval, return
    if root_node.left is not None, and root_node.left max is larger than x, go left
    otherwise, go right
    """
    if not root_node:
        return
    if root_node.low <= x.low and x.high <= root_node.high:
        return root_node
    left_node = root_node.left
    right_node = root_node.right
    if left_node and x.high <= left_node.max:
        return search_tree(left_node, x)
    return search_tree(right_node, x)

def search_interval(intervals, x):
    """
    iter over whole intervals and return intervals that contains x
    """
    LEFT = 0
    RIGHT = 1
    results = []
    for interval in intervals:
        if interval[LEFT] <= x.low and x.high <= interval[RIGHT]:
            results.append(interval)
    if results:
        return results
    return None

def test_build_tree():
    MAX = 100
    SIZE = 10
    intervals = create_intervals(MAX, SIZE)
    print("intervals:", intervals)
    print("=====================")
    result = build_tree(intervals)
    print("root: ", end="")
    pprint_tree(result)
    check_tree(result)
    print("check pass")

def create_intervals(max_num, size):
    intervals = []
    for _ in range(1, size):
        low = random.randint(1, max_num)
        high = random.randint(1, max_num)
        if low > high:
            low, high = high, low
        intervals.append((low, high))
    return intervals

def single_test():
    """
        #random several interval
        #random pick element
        #use interval tree find out if it's inside
        #use old fashion method to find out if it's inside
        #compare those two result
    """
    MAX = 100
    SIZE = 10
    intervals = create_intervals(MAX, SIZE)
    t = random.randint(1, MAX)
    target = TreeNode(t, t)
    root = build_tree(intervals)
    node = search_tree(root, target)
    intervals = search_interval(intervals, target)
    node_interval = node.to_interval() if node else None
    if not node_interval and not intervals:
        return
    if node_interval not in intervals:
        print("=======================")
        pprint_tree(root)
        print("target:", target)
        print("node interval:", node_interval)
        print("match intervals:", intervals)

def test():
    count = 1000
    for _ in range(count):
        single_test()

if __name__ == "__main__":
    test()
