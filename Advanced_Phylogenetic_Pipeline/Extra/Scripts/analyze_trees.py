import os
from ete3 import Tree
import json

# Arabidopsis MIKCc Clade Mapping
CLADES = {
    "AP1/FUL": ["AT1G24260", "AT1G69120", "AT5G60910"],
    "SEP": ["AT5G15800", "AT3G02310", "AT2G22590", "AT4G18050"],
    "AG": ["AT4G18960", "AT4G09960", "AT3G58780", "AT2G42830"],
    "SOC1": ["AT2G45660"],
    "SVP/AGL24": ["AT2G22540", "AT4G24540"],
    "FLC": ["AT5G10140"],
    "AP3/PI": ["AT3G54340", "AT5G20240"],
}

def analyze_tree(tree_path):
    if not os.path.exists(tree_path):
        return None
    
    try:
        t = Tree(tree_path)
    except:
        return None
    
    results = {}
    
    # Identify target species (those not containing AT)
    all_leaves = [l.name for l in t.iter_leaves()]
    target_leaves = [n for n in all_leaves if "AT" not in n]
    at_leaves = [n for n in all_leaves if "AT" in n]
    
    if not at_leaves:
        return None

    for clade_name, at_ids in CLADES.items():
        # Find leaves matching these AT IDs
        clade_at_nodes = []
        for leaf in t.iter_leaves():
            for aid in at_ids:
                if aid in leaf.name:
                    clade_at_nodes.append(leaf)
                    break
        
        if not clade_at_nodes:
            continue
            
        # Get the common ancestor of these AT nodes
        if len(clade_at_nodes) > 1:
            ancestor = t.get_common_ancestor(clade_at_nodes)
        else:
            ancestor = clade_at_nodes[0]
            
        # Find all target nodes within this clade (under the ancestor)
        clade_targets = [n.name for n in ancestor.iter_leaves() if "AT" not in n]
        
        if len(clade_targets) >= 2:
            # Analyze pattern: distances to the ancestor or each other
            distances = []
            for name in clade_targets:
                node = t.search_nodes(name=name)[0]
                dist = t.get_distance(ancestor, node)
                distances.append((name, dist))
            
            # Sort by distance
            distances.sort(key=lambda x: x[1])
            
            # Pattern check: Is one significantly further than the others?
            # Or is one basal (closer to the root of the clade) while others are specialized/together?
            results[clade_name] = {
                "targets": distances,
                "count": len(clade_targets)
            }
            
    return results

# Process all species
tree_files = [
    "./TASK_1/uploads/Rice_MADS_Domain_ML.treefile",
    "./TASK_2/uploads/Amborella_MADS_Domain_ML.treefile",
    "./TASK_3/uploads/Nymphaea_MADS_ML.treefile",
    "./TASK_4/uploads/Cinnamomum_MADS_ML.treefile",
    "./TASK_5/uploads/Glycine_MADS_ML.treefile",
    "./TASK_6/uploads/Medicago_MADS_ML.treefile",
    "./TASK_7/uploads/Prunus_MADS_ML.treefile",
    "./TASK_8/uploads/Helianthus_MADS_ML.treefile",
    "./TASK_9/uploads/Nelumbo_MADS_ML.treefile",
]

all_analysis = {}
os.chdir("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/")

for tf in tree_files:
    species = tf.split("/")[1]
    res = analyze_tree(tf)
    if res:
        all_analysis[species] = res

print(json.dumps(all_analysis, indent=2))
