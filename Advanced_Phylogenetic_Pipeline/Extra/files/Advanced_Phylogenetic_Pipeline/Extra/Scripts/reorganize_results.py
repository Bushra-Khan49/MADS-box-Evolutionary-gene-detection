import os, shutil

BASE_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection"
WORKFLOW_DIR = os.path.join(BASE_DIR, "Workflow_Step-by-Step")

# Sources
ML_TREE_SRC = os.path.join(BASE_DIR, "Advanced_Phylogenetic_Pipeline/3.Phylogeny_Output/Trees_FullLength")
ML_ALN_SRC = os.path.join(BASE_DIR, "Advanced_Phylogenetic_Pipeline/3.Phylogeny_Output/Alignments_FullLength")
ML_IMG_SRC = os.path.join(BASE_DIR, "Advanced_Phylogenetic_Pipeline/4.Visualization_Portfolio/Standardized_Trees")

# Legacy Sources (NJ/Bayes)
LEGACY_BASE = os.path.join(BASE_DIR, "Advanced_Phylogenetic_Pipeline/Archive/Legacy_Analysis_Folders/Simultaneous_Phylogenetic_Analysis/Results_v2")
NJ_SRC = os.path.join(LEGACY_BASE, "Trees/NJ")
BAYES_SRC = os.path.join(LEGACY_BASE, "Trees/Bayes")
ALN_SRC = os.path.join(LEGACY_BASE, "Alignments")

MAPPING = {
    "TASK_1": "Arabidopsis_thaliana",
    "TASK_2": "Amborella_trichopoda",
    "TASK_3": "Nymphaea_colorata",
    "TASK_4": "Cinnamomum_kanehirae",
    "TASK_5": "Oryza_sativa",
    "TASK_6": "Glycine_max",
    "TASK_7": "Medicago_truncatula",
    "TASK_8": "Prunus_persica",
    "TASK_9": "Helianthus_annuuss",
    "TASK_10": "Nelumbo_nucifera"
}

def reorganize():
    for task_id, species in MAPPING.items():
        uploads_dir = os.path.join(WORKFLOW_DIR, task_id, "uploads")
        if not os.path.exists(uploads_dir): continue
        
        # 1. Create subfolders
        ml_dir = os.path.join(uploads_dir, "ML")
        nj_dir = os.path.join(uploads_dir, "NJ")
        bayes_dir = os.path.join(uploads_dir, "Bayes")
        for d in [ml_dir, nj_dir, bayes_dir]: os.makedirs(d, exist_ok=True)
        
        # 2. Distribute ML Results (from current pipeline)
        algos = ["MAFFT", "MUSCLE", "ClustalO"]
        for algo in algos:
            # Treefile
            t_name = f"{species}_{algo}_ML.treefile"
            t_src = os.path.join(ML_TREE_SRC, t_name)
            if os.path.exists(t_src): shutil.copy2(t_src, os.path.join(ml_dir, t_name))
            
            # Alignment
            a_name = f"{species}_{algo}_Aligned.fa"
            a_src = os.path.join(ML_ALN_SRC, a_name)
            if os.path.exists(a_src): shutil.copy2(a_src, os.path.join(ml_dir, a_name))
            
            # PNG
            p_name = f"{species}_{algo}_Premium.png"
            p_src = os.path.join(ML_IMG_SRC, p_name)
            if os.path.exists(p_src): shutil.copy2(p_src, os.path.join(ml_dir, p_name))

        # 3. Distribute NJ Results (from legacy)
        for algo in algos:
            t_name = f"{species}_{algo}_NJ.treefile"
            t_src = os.path.join(NJ_SRC, t_name)
            if os.path.exists(t_src): shutil.copy2(t_src, os.path.join(nj_dir, t_name))
            
            a_name = f"{species}_{algo}.fa" # Legacy alignment naming
            a_src = os.path.join(ALN_SRC, a_name)
            if os.path.exists(a_src): shutil.copy2(a_src, os.path.join(nj_dir, a_name))

        # 4. Distribute Bayes Results (from legacy)
        for algo in algos:
            t_name = f"{species}_{algo}_Bayes.treefile"
            t_src = os.path.join(BAYES_SRC, t_name)
            if os.path.exists(t_src): shutil.copy2(t_src, os.path.join(bayes_dir, t_name))
            
            a_src = os.path.join(ALN_SRC, f"{species}_{algo}.fa")
            if os.path.exists(a_src): shutil.copy2(a_src, os.path.join(bayes_dir, f"{species}_{algo}.fa"))

        # 5. Cleanup flat files in root uploads (to avoid confusion)
        for item in os.listdir(uploads_dir):
            item_path = os.path.join(uploads_dir, item)
            if os.path.isfile(item_path) and ("Premium" in item or "treefile" in item):
                os.remove(item_path)

if __name__ == "__main__":
    reorganize()
