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

tasks = [
  ("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_1/uploads/Rice_MADS_Domain_ML.treefile", "Rice"),
  ("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_2/uploads/Amborella_MADS_Domain_ML.treefile", "Amborella"),
  ("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_3/uploads/Nymphaea_MADS_ML.treefile", "Nymphaea"),
  ("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_4/uploads/Cinnamomum_MADS_ML.treefile", "Cinnamomum"),
  ("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_5/uploads/Glycine_MADS_ML.treefile", "Glycine"),
  ("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_6/uploads/Medicago_MADS_ML.treefile", "Medicago"),
  ("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_7/uploads/Prunus_MADS_ML.treefile", "Prunus"),
  ("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_8/uploads/Helianthus_MADS_ML.treefile", "Helianthus"),
  ("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_9/uploads/Nelumbo_MADS_ML.treefile", "Nelumbo"),
]

with open("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/final_analysis_output.md", "w") as out:
    for tree_path, species in tasks:
        if not os.path.exists(tree_path):
            out.write(f"FAILED: {tree_path} not found\n")
            continue
        
        try:
            t = Tree(tree_path, format=1)
        except:
            out.write(f"FAILED: Could not parse {tree_path}\n")
            continue
            
        out.write(f"\n# {species} Phylogenetic Analysis\n")
        for clade_name, at_ids in CLADES.items():
            found_at = [l for l in t.iter_leaves() if any(aid in l.name for aid in at_ids)]
            if not found_at: continue
            
            try:
                anc = t.get_common_ancestor(found_at) if len(found_at) > 1 else found_at[0]
            except:
                continue
                
            targets = [l.name for l in anc.iter_leaves() if "AT" not in l.name]
            if len(targets) >= 2:
                # Analyze parent nodes recursively to find asymmetrical splits involving target species
                curr = anc
                pattern_found = False
                while curr and curr != t:
                    children = curr.get_children()
                    if len(children) == 2:
                        c1 = [l.name for l in children[0].iter_leaves() if "AT" not in l.name]
                        c2 = [l.name for l in children[1].iter_leaves() if "AT" not in l.name]
                        
                        if len(c1) == 1 and len(c2) >= 2:
                            out.write(f"- **{clade_name}**: Basal member  contrasts with derived cluster {c2}.\n")
                            pattern_found = True
                            break
                        elif len(c2) == 1 and len(c1) >= 2:
                            out.write(f"- **{clade_name}**: Basal member  contrasts with derived cluster {c1}.\n")
                            pattern_found = True
                            break
                    curr = curr.up
                if not pattern_found:
                    out.write(f"- **{clade_name}**: Generic expansion: {targets}\n")
            elif len(targets) == 1:
                out.write(f"- **{clade_name}**: Single ortholog: \n")
