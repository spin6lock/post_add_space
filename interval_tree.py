#!/usr/bin/env python3
#encoding:utf8

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
        return "max:{max}, interval:({low},{high})".format(
                max=self.max, low=self.low, high=self.high)

def insert_left_node(node, new):
    """
    insert to the correct place
    update max value as well
    """
    node.max = max(new.high, node.high)
    if node.left == None:
        node.left = new
    else: # insert into left subtree
        node = node.left
        if node.low < new.low:
            insert_left_node(node, new)
        else:
            insert_right_node(node, new)

def insert_right_node(node, new):
    """
    insert to the correct place
    update max value as well
    """
    node.max = max(new.high, node.high)
    if node.right == None:
        node.right = new
    else: # insert into left subtree
        node = node.right
        if node.low < new.low:
            insert_left_node(node, new)
        else:
            insert_right_node(node, new)

def traverse(node, func):
    func(node)
    if node.left:
        print("left")
        traverse(node.left, func)
    if node.right:
        print("right")
        traverse(node.right, func)

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
    root = TreeNode(intervals[1][0], intervals[1][1])
    for i in range(2, len(intervals)):
        interval = intervals[i]
        assert(interval[0] <= interval[1])
        new = TreeNode(interval[0], interval[1])
        if new.low < root.low:
            insert_left_node(root, new)
        else:
            insert_right_node(root, new)
    return root

def print_node(node):
    print(node)

def test_build_tree():
    intervals = create_intervals()
    print("intervals:", intervals)
    result = build_tree(intervals)
    traverse(result, print_node)

def create_intervals():
    MAX = 100
    size = 10
    intervals = []
    for i in range(1, size):
        low = random.randint(1, MAX)
        high = random.randint(low, MAX)
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

