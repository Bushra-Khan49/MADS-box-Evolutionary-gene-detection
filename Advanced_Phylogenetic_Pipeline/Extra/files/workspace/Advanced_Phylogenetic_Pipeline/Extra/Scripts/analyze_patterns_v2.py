import os
from ete3 import Tree

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
    base_path = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step"
    tree_path = os.path.join(base_path, species_task, "uploads", tree_file)
    
    if not os.path.exists(tree_path):
        return
    
    try:
        t = Tree(tree_path)
    except Exception as e:
        print(f"Error loading {tree_path}: {e}")
        return
    
    print(f"\n# Analysis for {species_task} ({tree_file})")
    
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
            try:
                anc = t.get_common_ancestor(found_at)
            except:
                anc = found_at[0]
        else:
            anc = found_at[0]
            
        # Get target leaves in this clade (up to the parent of anc to catch basal targets)
        # To find "Separate" (basal) members, we often need to look at the siblings of the main AT group
        targets = [l.name for l in anc.iter_leaves() if "AT" not in l.name]
        
        # Pattern Detection Strategy:
        # Check if the ancestor of the clade has a very asymmetrical split
        # OR if one target is significantly closer to the root of the clade than others
        if len(targets) >= 2:
            children = anc.get_children()
            if len(children) == 2:
                c1_targets = [l.name for l in children[0].iter_leaves() if "AT" not in l.name]
                c2_targets = [l.name for l in children[1].iter_leaves() if "AT" not in l.name]
                
                if len(c1_targets) == 1 and len(c2_targets) >= 2:
                    print(f"- **{clade_name}**: Basal member  contrasts with expanded cluster {c2_targets}.")
                elif len(c2_targets) == 1 and len(c1_targets) >= 2:
                    print(f"- **{clade_name}**: Basal member  contrasts with expanded cluster {c1_targets}.")
                else:
                    print(f"- **{clade_name}**: Multiple members found: {targets}")
            else:
                print(f"- **{clade_name}**: targets found: {targets}")
        elif len(targets) == 1:
            print(f"- **{clade_name}**: Single ortholog detected: ")

# Detect all tree files
base_path = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step"
for root, dirs, files in os.walk(base_path):
    for f in files:
        if f.endswith("_MADS_ML.treefile") or f.endswith("_MADS_Domain_ML.treefile"):
            task_dir = os.path.basename(os.path.dirname(os.path.dirname(os.path.join(root, f))))
            if task_dir.startswith("TASK_"):
                 analyze_species(task_dir, f)
