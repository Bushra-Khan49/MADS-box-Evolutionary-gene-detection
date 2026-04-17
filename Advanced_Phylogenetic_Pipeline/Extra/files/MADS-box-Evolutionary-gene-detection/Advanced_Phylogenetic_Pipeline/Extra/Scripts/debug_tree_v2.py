import os
from ete3 import Tree

def debug_tree(tree_file):
    if not os.path.exists(tree_file):
        print(f"File not found: {tree_file}")
        return
    
    with open(tree_file, "r") as f:
        content = f.read()
    
    print(f"Content length: {len(content)}")
    
    try:
        t = Tree(tree_file, format=1)
        print(f"Tree loaded successfully with format=1")
    except Exception as e1:
        try:
            t = Tree(tree_file, format=0)
            print(f"Tree loaded successfully with format=0")
        except Exception as e2:
            print(f"Failed to load tree: {e1} | {e2}")
            return
            
    at_nodes = [l.name for l in t.iter_leaves() if "AT" in l.name]
    print(f"Found {len(at_nodes)} AT nodes")
    for n in at_nodes[:5]:
        print(f"  {n}")

debug_tree("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_7/uploads/Prunus_MADS_ML.treefile")
