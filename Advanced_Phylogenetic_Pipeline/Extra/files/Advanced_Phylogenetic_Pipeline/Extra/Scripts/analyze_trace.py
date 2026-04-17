import os, sys
from ete3 import Tree

tree_path = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_7/uploads/Prunus_MADS_ML.treefile"

if not os.path.exists(tree_path):
    print(f"ERROR: {tree_path} not found")
    sys.exit(1)

try:
    print(f"Loading {tree_path}...")
    t = Tree(tree_path, format=1)
    print(f"Success! Leaves: {len(t)}")
    at_nodes = [l for l in t.iter_leaves() if "AT" in l.name]
    print(f"AT nodes found: {len(at_nodes)}")
    
    # Try getting common ancestor of a known clade (e.g. SOC1)
    soc1_at = [l for l in t.iter_leaves() if "AT2G45660" in l.name]
    if soc1_at:
        print(f"SOC1 AT found: {soc1_at[0].name}")
        anc = soc1_at[0].up
        if anc:
            targets = [l.name for l in anc.iter_leaves() if "AT" not in l.name]
            print(f"Targets near SOC1 AT: {targets}")
except Exception as e:
    print(f"EXCEPTION: {e}")
