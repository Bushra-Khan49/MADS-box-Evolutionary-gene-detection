import os
import subprocess
import concurrent.futures

# Configuration
WORKSPACE = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Simultaneous_Phylogenetic_Analysis"
DATASET_DIR = os.path.join(WORKSPACE, "Datasets/Merged")
ALIGN_DIR = os.path.join(WORKSPACE, "Results_v2/Alignments")
NJ_TREE_DIR = os.path.join(WORKSPACE, "Results_v2/Trees/NJ")
BAYES_TREE_DIR = os.path.join(WORKSPACE, "Results_v2/Trees/Bayes")
IQTREE_BIN = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Advanced_Phylogenetic_Pipeline/Uploads/scripts/iqtree2"

os.makedirs(ALIGN_DIR, exist_ok=True)
os.makedirs(NJ_TREE_DIR, exist_ok=True)
os.makedirs(BAYES_TREE_DIR, exist_ok=True)

SPECIES_FILES = [f for f in os.listdir(DATASET_DIR) if f.endswith(".fa")]

def run_cmd(cmd, shell=True):
    print(f"Executing: {cmd}")
    try:
        subprocess.run(cmd, shell=shell, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing {cmd}: {e.stderr.decode()}")
        return False

def process_species(species_fa):
    species_name = species_fa.replace(".fa", "")
    input_path = os.path.join(DATASET_DIR, species_fa)
    
    # 1. Triple Alignment
    alignments = {
        "MAFFT": os.path.join(ALIGN_DIR, f"{species_name}_MAFFT.fa"),
        "MUSCLE": os.path.join(ALIGN_DIR, f"{species_name}_MUSCLE.fa"),
        "ClustalO": os.path.join(ALIGN_DIR, f"{species_name}_ClustalO.fa")
    }
    
    run_cmd(f"mafft --auto {input_path} > {alignments['MAFFT']}")
    run_cmd(f"muscle -align {input_path} -output {alignments['MUSCLE']}")
    run_cmd(f"clustalo -i {input_path} -o {alignments['ClustalO']}")
    
    # 2. Dual Phylogeny per Alignment
    for algo, al_path in alignments.items():
        if not os.path.exists(al_path): continue
        
        # Phylogeny A: NJ (BIONJ) specifically
        nj_prefix = os.path.join(NJ_TREE_DIR, f"{species_name}_{algo}_NJ")
        run_cmd(f"{IQTREE_BIN} -s {al_path} -m LG -n 0 -pre {nj_prefix} -redo")
        
        # Phylogeny B: Bayesian-like (aBayes) with 1000 Support
        bayes_prefix = os.path.join(BAYES_TREE_DIR, f"{species_name}_{algo}_Bayes")
        run_cmd(f"{IQTREE_BIN} -s {al_path} -fast -alrt 1000 -abayes -pre {bayes_prefix} -redo")

if __name__ == "__main__":
    print(f"Starting simultaneous batch for {len(SPECIES_FILES)} species...")
    # Sequential processing: 1 species at a time for maximum stability
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(process_species, sorted(SPECIES_FILES))
    print("Batch processing complete.")
