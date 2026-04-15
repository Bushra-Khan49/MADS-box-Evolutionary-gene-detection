import os
from ete3 import Tree
import json

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
        t = Tree(tree_path, format=1)
    except:
        return None
    
    results = {}
    for clade_name, at_ids in CLADES.items():
        found_at = [l for l in t.iter_leaves() if any(aid in l.name for aid in at_ids)]
        if not found_at: continue
        
        try:
            anc = t.get_common_ancestor(found_at) if len(found_at) > 1 else found_at[0]
        except:
            continue
            
        targets = [l.name for l in anc.iter_leaves() if "AT" not in l.name]
        clade_res = {"targets": targets, "pattern": "None", "basal": [], "expanded": []}
        
        if len(targets) >= 2:
            # Check for "Separate vs Together" pattern
            curr = anc
            while curr and curr != t:
                children = curr.get_children()
                if len(children) == 2:
                    c1 = [l.name for l in children[0].iter_leaves() if "AT" not in l.name]
                    c2 = [l.name for l in children[1].iter_leaves() if "AT" not in l.name]
                    
                    if len(c1) == 1 and len(c2) >= 2:
                        clade_res["pattern"] = "Basal Divergence"
                        clade_res["basal"] = c1
                        clade_res["expanded"] = c2
                        break
                    elif len(c2) == 1 and len(c1) >= 2:
                        clade_res["pattern"] = "Basal Divergence"
                        clade_res["basal"] = c2
                        clade_res["expanded"] = c1
                        break
                curr = curr.up
        
        results[clade_name] = clade_res
    return results

tasks = [
    ("TASK_1", "Rice_MADS_Domain_ML.treefile"),
    ("TASK_2", "Amborella_MADS_Domain_ML.treefile"),
    ("TASK_3", "Nymphaea_MADS_ML.treefile"),
    ("TASK_4", "Cinnamomum_MADS_ML.treefile"),
    ("TASK_5", "Glycine_MADS_ML.treefile"),
    ("TASK_6", "Medicago_MADS_ML.treefile"),
    ("TASK_7", "Prunus_MADS_ML.treefile"),
    ("TASK_8", "Helianthus_MADS_ML.treefile"),
    ("TASK_9", "Nelumbo_MADS_ML.treefile"),
]

all_results = {}
base_dir = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step"

for task, tf in tasks:
    res = analyze_tree(os.path.join(base_dir, task, "uploads", tf))
    if res:
        all_results[task] = res

print(json.dumps(all_results, indent=2))
