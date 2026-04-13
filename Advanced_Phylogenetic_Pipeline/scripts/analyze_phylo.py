from Bio import Phylo
import os

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

for tree_path, species in tasks:
    if not os.path.exists(tree_path): continue
    
    print(f"\n# {species} Analysis")
    tree = Phylo.read(tree_path, "newick")
    
    for clade_name, at_ids in CLADES.items():
        found_at = [l for l in tree.get_terminals() if any(aid in l.name for aid in at_ids)]
        if not found_at: continue
        
        mrca = tree.common_ancestor(found_at)
        targets = [l.name for l in mrca.get_terminals() if "AT" not in l.name]
        
        if len(targets) >= 2:
            # Check for pattern
            target_nodes = [l for l in mrca.get_terminals() if "AT" not in l.name]
            # Simple check: is one target's parent the MRCA while others are deeper?
            basal = []
            derived = []
            for t_node in target_nodes:
                path = mrca.get_path(t_node)
                if len(path) == 1: # Immediate child of MRCA
                    basal.append(t_node.name)
                else:
                    derived.append(t_node.name)
            
            if len(basal) == 1 and len(derived) >= 1:
                print(f"- **{clade_name}**: Basal Member  | Cluster {derived}")
            else:
                print(f"- **{clade_name}**: Targets {targets}")
        elif len(targets) == 1:
            print(f"- **{clade_name}**: Ortholog {targets[0]}")
