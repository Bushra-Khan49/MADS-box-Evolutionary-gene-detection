import os
from ete3 import Tree

tree_path = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_7/uploads/Prunus_MADS_ML.treefile"
t = Tree(tree_path, format=1)
print(f"Total Leaves: {len(t)}")
at_nodes = [l.name for l in t.iter_leaves() if "AT" in l.name]
print(f"Total AT Nodes: {len(at_nodes)}")
for n in at_nodes[:5]:
    print(f"AT Node: {n}")
