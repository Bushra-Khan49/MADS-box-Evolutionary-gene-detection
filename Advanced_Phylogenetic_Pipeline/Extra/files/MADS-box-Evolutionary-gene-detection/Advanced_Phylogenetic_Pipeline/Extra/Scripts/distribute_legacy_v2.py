import os
import shutil

# Paths
BASE_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection"
WORKFLOW_DIR = os.path.join(BASE_DIR, "Workflow_Step-by-Step")
LEGACY_VISUALS_DIR = os.path.join(BASE_DIR, "Advanced_Phylogenetic_Pipeline/Archive/Legacy_Analysis_Folders/Unified_Phylogenetic_Tree_Collection/Simultaneous_Analysis")
LEGACY_TREES_DIR = os.path.join(BASE_DIR, "Advanced_Phylogenetic_Pipeline/Archive/Legacy_Analysis_Folders/Simultaneous_Phylogenetic_Analysis/Results/Trees")
LEGACY_ALIGNMENTS_DIR = os.path.join(BASE_DIR, "Advanced_Phylogenetic_Pipeline/Archive/Legacy_Analysis_Folders/Simultaneous_Phylogenetic_Analysis/Results/Alignments")

# Species to TASK Mapping
SPECIES_MAP = {
    "Arabidopsis_thaliana": "TASK_1",
    "Amborella_trichopoda": "TASK_2",
    "Nymphaea_colorata": "TASK_3",
    "Cinnamomum_kanehirae": "TASK_4",
    "Oryza_sativa": "TASK_5",
    "Glycine_max": "TASK_6",
    "Medicago_truncatula": "TASK_7",
    "Prunus_persica": "TASK_8",
    "Helianthus_annuuss": "TASK_9",
    "Nelumbo_nucifera": "TASK_10"
}

def distribute_legacy():
    for species, task_id in SPECIES_MAP.items():
        print(f"Processing {species} -> {task_id}...")
        
        task_root = os.path.join(WORKFLOW_DIR, task_id, "uploads")
        visuals_target = os.path.join(task_root, "2.Tree_Visualizations")
        trees_target = os.path.join(task_root, "1.Phylogenetic_Trees")
        alignments_target = os.path.join(task_root, "3.Sequence_Alignments")

        # Create target directories if they don't exist
        for d in [visuals_target, trees_target, alignments_target]:
            os.makedirs(d, exist_ok=True)

        # 1. Visualizations
        spec_visual_dir = os.path.join(LEGACY_VISUALS_DIR, species)
        if os.path.exists(spec_visual_dir):
            for f in os.listdir(spec_visual_dir):
                if f.endswith(".png"):
                    shutil.copy2(os.path.join(spec_visual_dir, f), os.path.join(visuals_target, f))
                    print(f"  Copied Visualization: {f}")

        # 2. Tree Files (NJ and Bayes)
        for method in ["NJ", "Bayes"]:
            method_dir = os.path.join(LEGACY_TREES_DIR, method)
            if os.path.exists(method_dir):
                for f in os.listdir(method_dir):
                    if f.startswith(species) and (f.endswith(".treefile") or f.endswith(".nwk")):
                        shutil.copy2(os.path.join(method_dir, f), os.path.join(trees_target, f))
                        print(f"  Copied Tree ({method}): {f}")

        # 3. Alignments
        if os.path.exists(LEGACY_ALIGNMENTS_DIR):
            for f in os.listdir(LEGACY_ALIGNMENTS_DIR):
                if f.startswith(species) and f.endswith(".fa"):
                    shutil.copy2(os.path.join(LEGACY_ALIGNMENTS_DIR, f), os.path.join(alignments_target, f))
                    print(f"  Copied Alignment: {f}")

if __name__ == "__main__":
    distribute_legacy()
