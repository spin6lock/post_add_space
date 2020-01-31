#!/usr/bin/env python3
#encoding:utf8

import argparse
import interval_tree
search_tree = interval_tree.search_tree
TreeNode = interval_tree.TreeNode

cjk_range = [
    (u'\u3040', u'\u309F'),    # Japanese Hiragana
    (u'\u30A0', u'\u30FF'),    # Japanese Katakana
    (u'\u3400', u'\u4DB5'),    # CJK Unified Ideographs Extension A
    (u'\u4E00', u'\u9FEF'),    # CJK Unified Ideographs
    (u'\uF900', u'\uFAFF'),    # CJK Compatibility Ideographs
    (u'\U00020000', u'\U0002A6D6'),  # CJK Unified Ideographs Extension B
    (u'\U0002A700', u'\U0002B734'),  # CJK Unified Ideographs Extension C
    (u'\U0002b740', u'\U0002B81D'),  # CJK Unified Ideographs Extension D
    (u'\U0002B820', u'\U0002CEA1'),  # CJK Unified Ideographs Extension E
    (u'\U0002ceb0', u'\U0002EBE0'),  # CJK Unified Ideographs Extension F
    (u'\U0002F800', u'\U0002FA1F'),  # CJK Compatibility Ideographs Supplement
]

cjk_tree = interval_tree.build_tree(cjk_range)
def is_cjk(char):
    return search_tree(cjk_tree, TreeNode(char, char))

punc_range = [
    (u'\u0000', u'\u0020'),  # space
    (u'\u003c', u'\u003c'),  # less-than sign
    (u'\u003e', u'\u003e'),  # grater-than sign
    (u'\u3000', u'\u303f'),  # CJK Symbols and Punctuation
    (u'\uff00', u'\uffef'),  # Halfwidth and Fullwidth Forms
    (u'\u200D', u'\u200D'),           # ZERO WIDTH JOINER
    (u'\uFE0E', u'\uFE0F'),           # VARIATION SELECTOR-15/16
]

punc_tree = interval_tree.build_tree(punc_range)
def is_punc(char):
    return search_tree(punc_tree, TreeNode(char, char))

def process(content):
    ret = []
    prev = None
    sp = ' '
    for char in content:
        curr_is_cjk = is_cjk(char)
        curr_is_punc = is_punc(char)
        if prev:
            prev_is_cjk, prev_is_punc = prev
            if prev_is_punc or curr_is_punc:
                #ret.append(char)
                pass
            elif prev_is_cjk != curr_is_cjk:
                ret.append(sp)
        ret.append(char)
        prev = (curr_is_cjk, curr_is_punc)
    return ''.join(ret)


def main():
    parser = argparse.ArgumentParser("add space between cjk Character and ASCII")
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    with open(filename, "r") as fh:
        content = fh.read()
    new_content = process(content)
    with open(filename, "w") as fh:
        fh.write(new_content)

if __name__ == "__main__":
    main()
