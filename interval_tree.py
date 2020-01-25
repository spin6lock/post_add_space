#!/usr/bin/env python3
#encoding:utf8

from treelib import Node, Tree
import random

"""
This module provide interface to build a interval
tree. Also with the search API to decide whether 
an interval is inside.
"""

class TreeNode():
    def __init__(self, low, high):
        self.low = low
        self.high = high
        self.left = None
        self.right = None
        self.max = 0

    def __str__(self):
        return "[{low},{high}], max:{max}".format(
                max=self.max, low=self.low, high=self.high)

def insert_node(node, direct, new):
    """
    insert to the correct place
    update max value as well
    """
    node.max = max(new.high, node.high, node.max)
    if getattr(node, direct) == None:
        setattr(node, direct, new)
    else: # insert into left subtree
        node = getattr(node, direct)
        if new.low < node.low:
            insert_node(node, "left", new)
        else:
            insert_node(node, "right", new)

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
    assert(len(intervals) > 0)
    root_interval = intervals[0]
    root = TreeNode(root_interval[0], root_interval[1])
    for i in range(2, len(intervals)):
        interval = intervals[i]
        assert(interval[0] <= interval[1])
        new = TreeNode(interval[0], interval[1])
        new.max = new.high
        if new.low < root.low:
            insert_node(root, "left", new)
        else:
            insert_node(root, "right", new)
    return root

def check_tree(root_node):
    assert(root_node)
    if root_node.left:
        left_node = root_node.left
        assert(left_node.low < root_node.low)
        assert(left_node.max <= root_node.max)
        check_tree(left_node)
    if root_node.right:
        right_node = root_node.right
        assert(right_node.low >= root_node.low)
        assert(right_node.max <= root_node.max)
        check_tree(right_node)

def test_build_tree():
    intervals = create_intervals()
    print("intervals:", intervals)
    print("=====================")
    result = build_tree(intervals)
    print("root: ", end="")
    pprint_tree(result)
    check_tree(result)
    print("check pass")

def create_intervals():
    MAX = 100
    size = 10
    intervals = []
    for i in range(1, size):
        low = random.randint(1, MAX)
        high = random.randint(1, MAX)
        if low > high:
            low, high = high, low
        intervals.append((low, high))
    return intervals

"""
    #random several interval
    #random pick element
    #use interval tree find out if it's inside
    #use old fashion method to find out if it's inside
    #compare those two result
"""
def test():
    pass

if __name__ == "__main__":
    test_build_tree()

