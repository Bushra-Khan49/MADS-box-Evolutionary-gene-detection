import os, shutil

BASE_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection"
TREE_SRC = os.path.join(BASE_DIR, "Advanced_Phylogenetic_Pipeline/3.Phylogeny_Output/Trees_FullLength")
IMG_SRC = os.path.join(BASE_DIR, "Advanced_Phylogenetic_Pipeline/4.Visualization_Portfolio/Standardized_Trees")
WORKFLOW_DIR = os.path.join(BASE_DIR, "Workflow_Step-by-Step")

# Finalized Species-to-Task Mapping
MAPPING = {
    "Amborella_trichopoda": "TASK_2",
    "Nymphaea_colorata":    "TASK_3",
    "Cinnamomum_kanehirae": "TASK_4",
    "Oryza_sativa":         "TASK_5",
    "Glycine_max":          "TASK_6",
    "Medicago_truncatula":  "TASK_7",
    "Prunus_persica":       "TASK_8",
    "Helianthus_annuuss":   "TASK_9",
    "Nelumbo_nucifera":     "TASK_10",
    "Piper_auritum":        "TASK_11"
}

def distribute_results():
    for species, task in MAPPING.items():
        dest_dir = os.path.join(WORKFLOW_DIR, task, "uploads")
        os.makedirs(dest_dir, exist_ok=True)
        
        algos = ["MAFFT", "MUSCLE", "ClustalO"]
        
        for algo in algos:
            # 1. Newick Treefile
            tree_name = f"{species}_{algo}_ML.treefile"
            tree_path = os.path.join(TREE_SRC, tree_name)
            if os.path.exists(tree_path):
                shutil.copy2(tree_path, os.path.join(dest_dir, tree_name))
                print(f"Copied {tree_name} -> {task}/uploads/")
            
            # 2. Premium PNG Visualization
            img_name = f"{species}_{algo}_Premium.png"
            img_path = os.path.join(IMG_SRC, img_name)
            if os.path.exists(img_path):
                shutil.copy2(img_path, os.path.join(dest_dir, img_name))
                print(f"Copied {img_name} -> {task}/uploads/")
                
if __name__ == "__main__":
    distribute_results()
