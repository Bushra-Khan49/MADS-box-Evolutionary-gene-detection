import os
import subprocess
import sys

def run_cmd(cmd, cwd=None):
    # print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error executing command: {cmd}\nStderr: {result.stderr}", file=sys.stderr)
    return result.stdout

def process_species_tree(working_dir, species_name, at_ref_fasta):
    print(f"--- Building individual tree for {species_name} ---")
    spec_dir = os.path.join(working_dir, species_name)
    candidates_fa = os.path.join(spec_dir, f"{species_name}_candidates.fa")
    
    if not os.path.exists(candidates_fa):
        print(f"Candidates FASTA not found for {species_name}")
        return

    # 1. Combine with Arabidopsis
    combined_fa = os.path.join(spec_dir, f"{species_name}_with_AT.fa")
    with open(combined_fa, 'w') as fout:
        with open(candidates_fa, 'r') as fc: fout.write(fc.read())
        with open(at_ref_fasta, 'r') as fa: fout.write(fa.read())

    # 2. Align with MAFFT
    aligned_fa = os.path.join(spec_dir, f"{species_name}_aligned.fa")
    run_cmd(f"/opt/homebrew/bin/mafft --auto {combined_fa} > {aligned_fa}")

    # 3. Run IQ-TREE 2
    iqtree_bin = "/Users/bushrakhan/Desktop/NIPGR-data/NIPGR_WORK/scripts/iqtree2"
    tree_cmd = [
        iqtree_bin,
        "-s", aligned_fa,
        "-m", "LG+G",
        "-bb", "1000",
        "-T", "2",
        "--redo"
    ]
    
    print(f"  Running IQ-TREE for {species_name}...")
    result = subprocess.run(tree_cmd, cwd=spec_dir, capture_output=True, text=True)
    
    if os.path.exists(f"{aligned_fa}.treefile"):
        print(f"  Successfully built tree for {species_name}")
    else:
        print(f"  Failed to build tree for {species_name}")
        print(result.stderr)

if __name__ == "__main__":
    # Correct paths for workspace
    base_dir = "/Users/bushrakhan/Desktop/NIPGR-data/NIPGR_WORK"
    at_ref = "/Users/bushrakhan/Desktop/NIPGR-data/TASK_4/Brapa_vs_Athaliana/ATH_MADS.domains.fa"
    
    species_list = [
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
    
    for species in species_list:
        process_species_tree(base_dir, species, at_ref)

    print("\nBatch tree building finished.")
