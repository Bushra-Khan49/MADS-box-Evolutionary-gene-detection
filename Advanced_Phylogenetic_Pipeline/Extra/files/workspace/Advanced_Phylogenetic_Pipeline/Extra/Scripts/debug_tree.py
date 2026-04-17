import os
from ete3 import Tree

def debug_tree(tree_file):
    if not os.path.exists(tree_file):
        print(f"File not found: {tree_file}")
        return
    
    t = Tree(tree_file)
    print(f"Tree: {tree_file}")
    for leaf in t.iter_leaves():
        if "AT" in leaf.name:
            print(f"Found AT: {leaf.name}")

debug_tree("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_7/uploads/Prunus_MADS_ML.treefile")
