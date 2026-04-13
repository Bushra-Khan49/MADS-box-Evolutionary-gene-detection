import os
import subprocess
import shutil

# Paths
WORKSPACE = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Simultaneous_Phylogenetic_Analysis"
ALIGN_DIR = os.path.join(WORKSPACE, "Results/Alignments")
TARGET_NJ_DIR = os.path.join(WORKSPACE, "Results_v2/Trees/NJ")
TARGET_BAYES_DIR = os.path.join(WORKSPACE, "Results_v2/Trees/Bayes")
IQTREE_BIN = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Advanced_Phylogenetic_Pipeline/Uploads/scripts/iqtree2"

# Ensure target directories exist
os.makedirs(TARGET_NJ_DIR, exist_ok=True)
os.makedirs(TARGET_BAYES_DIR, exist_ok=True)

def get_disk_space():
    stat = os.statvfs('/')
    return (stat.f_bavail * stat.f_frsize) / (1024**3)

def run_cmd(cmd):
    print(f"Executing: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False

def cleanup_checkpoints(prefix):
    for ext in [".ckp.gz", ".log", ".mldist", ".model.gz"]:
        file_path = prefix + ext
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Cleaned up: {file_path}")

def process_alignment(al_file):
    species_algo = al_file.replace(".fa", "")
    al_path = os.path.join(ALIGN_DIR, al_file)
    
    print(f"\n=== Processing {species_algo} ===")
    print(f"Remaining Disk: {get_disk_space():.2f} GiB")
    
    if get_disk_space() < 1.0:
        print("CRITICAL: Disk space below 1GiB. Stopping.")
        return False
    
    # Run NJ Tree
    nj_prefix = os.path.join(TARGET_NJ_DIR, f"{species_algo}_NJ")
    run_cmd(f"{IQTREE_BIN} -s {al_path} -m LG -n 0 -pre {nj_prefix} -redo")
    cleanup_checkpoints(nj_prefix)
    
    # Run Bayes Tree
    bayes_prefix = os.path.join(TARGET_BAYES_DIR, f"{species_algo}_Bayes")
    run_cmd(f"{IQTREE_BIN} -s {al_path} -fast -alrt 1000 -abayes -pre {bayes_prefix} -redo")
    cleanup_checkpoints(bayes_prefix)
    
    return True

if __name__ == "__main__":
    # Skip MAFFT as those are already complete; focus on MUSCLE and ClustalO
    all_files = os.listdir(ALIGN_DIR)
    alignments = sorted([f for f in all_files if f.endswith(".fa") and ("MUSCLE" in f or "ClustalO" in f)])
    
    print(f"--- Moving to MUSCLE & Clustal Omega Tree Generation ---")
    print(f"Found {len(alignments)} target alignment files.")
    
    for al in alignments:
        success = process_alignment(al)
        if not success:
            break
            
    print("\nBatch process finished.")
