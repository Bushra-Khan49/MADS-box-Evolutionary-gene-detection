import os
from ete3 import Tree

# Simplified Clade Mapping
CLADES = {
    "AP1/FUL": ["AT1G24260", "AT1G69120", "AT5G60910"],
    "SEP": ["AT5G15800", "AT3G02310", "AT2G22590", "AT4G18050"],
    "AG": ["AT4G18960", "AT4G09960", "AT3G58780", "AT2G42830"],
    "SOC1": ["AT2G45660"],
    "SVP/AGL24": ["AT2G22540", "AT4G24540"],
    "FLC": ["AT5G10140"],
    "AP3/PI": ["AT3G54340", "AT5G20240"],
}

def analyze_species(species_task, tree_file):
    tree_path = f"/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/{species_task}/uploads/{tree_file}"
    if not os.path.exists(tree_path):
        return
    
    try:
        t = Tree(tree_path)
    except:
        return
    
    print(f"\n--- Analysis for {species_task} ({tree_file}) ---")
    
    for clade_name, at_ids in CLADES.items():
        found_at = []
        for leaf in t.iter_leaves():
            for aid in at_ids:
                if aid in leaf.name:
                    found_at.append(leaf)
                    break
        
        if not found_at:
            continue
            
        if len(found_at) > 1:
            anc = t.get_common_ancestor(found_at)
        else:
            anc = found_at[0]
            
        # Get target leaves in this clade
        targets = [l.name for l in anc.iter_leaves() if "AT" not in l.name]
        
        if len(targets) >= 2:
            # Look for "One Separate, Rest Together"
            # We look at the first split of the anc
            children = anc.get_children()
            if len(children) == 2:
                c1_targets = [l.name for l in children[0].iter_leaves() if "AT" not in l.name]
                c2_targets = [l.name for l in children[1].iter_leaves() if "AT" not in l.name]
                
                if (len(c1_targets) == 1 and len(c2_targets) > 1):
                    print(f"[{clade_name}] Pattern Detected: {c1_targets[0]} (Basal) vs {c2_targets} (Expanded)")
                elif (len(c2_targets) == 1 and len(c1_targets) > 1):
                    print(f"[{clade_name}] Pattern Detected: {c2_targets[0]} (Basal) vs {c1_targets} (Expanded)")
                else:
                    # Generic expansion
                    print(f"[{clade_name}] Multiple members: {targets}")
            else:
                 print(f"[{clade_name}] Complex split: {targets}")
        elif len(targets) == 1:
            print(f"[{clade_name}] Single member: {targets[0]}")

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

for task, tf in tasks:
    analyze_species(task, tf)
