import os
import subprocess
import shutil

NIPGR_WORK_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/NIPGR_WORK"
RESULTS_DIR = os.path.abspath("Results_v4")

# List of species available
SPECIES_LIST = [
    "Amborella_trichopoda",
    "Cinnamomum_kanehirae",
    "Glycine_max",
    "Helianthus_annuuss",
    "Medicago_truncatula",
    "Nelumbo_nucifera",
    "Nymphaea_colorata",
    "Oryza_sativa",
    "Prunus_persica"
]

def extract_at_references():
    """Extracts exactly the AT reference sequences (109 MADS ones) from a reliable merged file."""
    ref_file = os.path.join(NIPGR_WORK_DIR, "Prunus_persica", "Prunus_persica_with_AT.fa")
    out_file = os.path.join(RESULTS_DIR, "AT_Diligent_Candidates.fa")
    
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    at_sequences = []
    current_header = ""
    current_seq = []
    
    if not os.path.exists(ref_file):
        print(f"ERROR: Cannot find reference {ref_file}")
        return None
        
    with open(ref_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if line.startswith(">"):
                if current_header and current_header.upper().startswith(">AT"):
                    at_sequences.append((current_header, "".join(current_seq)))
                current_header = line
                current_seq = []
            else:
                current_seq.append(line)
                
    if current_header and current_header.upper().startswith(">AT"):
        at_sequences.append((current_header, "".join(current_seq)))
        
    with open(out_file, "w") as f:
        for header, seq in at_sequences:
            f.write(f"{header}\n{seq}\n")
            
    print(f"Extracted {len(at_sequences)} AT anchor sequences to {out_file}")
    return out_file

def run_msa(input_fa, out_mafft, out_muscle, out_clustalo):
    # MAFFT
    print("Running MAFFT...")
    with open(out_mafft, "w") as f_out:
        subprocess.run(["mafft", "--auto", input_fa], stdout=f_out, stderr=subprocess.DEVNULL)
        
    # MUSCLE
    print("Running MUSCLE...")
    subprocess.run(["muscle", "-align", input_fa, "-output", out_muscle], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Clustal Omega
    print("Running Clustal Omega...")
    subprocess.run(["clustalo", "-i", input_fa, "-o", out_clustalo, "--force"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_iqtree(msa_file, prefix, method):
    if method == "nj":
        cmd = ["iqtree2", "-s", msa_file, "-fast", "-m", "BIONJ", "-B", "1000", "-pre", prefix, "-redo"]
    elif method == "abayes":
        cmd = ["iqtree2", "-s", msa_file, "-m", "MFP", "-B", "1000", "--abayes", "-pre", prefix, "-redo"]
    else:
        return
        
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error running IQ-TREE for {prefix}: {e}")

def process_species(species, at_ref_file):
    print(f"\n[{species}] Starting processing...")
    
    species_cand_file = os.path.join(NIPGR_WORK_DIR, species, f"{species}_candidates.fa")
    if not os.path.exists(species_cand_file):
        print(f"  -> ERROR: {species_cand_file} not found. Skipping.")
        return
        
    out_dir = os.path.join(RESULTS_DIR, species)
    os.makedirs(out_dir, exist_ok=True)
    
    merged_fa = os.path.join(out_dir, f"{species}_merged_input.fa")
    
    # 1. Merge
    print("  -> Creating Contextual Merge...")
    with open(merged_fa, "w") as out_f, open(species_cand_file, "r") as sp_f, open(at_ref_file, "r") as at_f:
        out_f.write(sp_f.read().strip() + "\n")
        out_f.write(at_f.read().strip() + "\n")
        
    # 2. MSA
    print("  -> Running Triple Alignment...")
    mafft_out = os.path.join(out_dir, f"{species}_MAFFT.fa")
    muscle_out = os.path.join(out_dir, f"{species}_MUSCLE.fa")
    clustal_out = os.path.join(out_dir, f"{species}_ClustalO.fa")
    run_msa(merged_fa, mafft_out, muscle_out, clustal_out)
    
    # 3. Phylogeny
    print("  -> Constructing NJ Trees...")
    run_iqtree(mafft_out, os.path.join(out_dir, f"{species}_MAFFT_NJ"), "nj")
    run_iqtree(muscle_out, os.path.join(out_dir, f"{species}_MUSCLE_NJ"), "nj")
    run_iqtree(clustal_out, os.path.join(out_dir, f"{species}_ClustalO_NJ"), "nj")
    
    print("  -> Constructing Bayesian Trees...")
    run_iqtree(mafft_out, os.path.join(out_dir, f"{species}_MAFFT_Bayes"), "abayes")
    run_iqtree(muscle_out, os.path.join(out_dir, f"{species}_MUSCLE_Bayes"), "abayes")
    run_iqtree(clustal_out, os.path.join(out_dir, f"{species}_ClustalO_Bayes"), "abayes")
    
    print(f"[{species}] Completely processed.")

if __name__ == "__main__":
    print(f"Output directory: {RESULTS_DIR}")
    at_ref = extract_at_references()
    if not at_ref:
        exit(1)
        
    for sp in SPECIES_LIST:
        process_species(sp, at_ref)
        
    print("\n--- BATCH COMPLETE ---")
