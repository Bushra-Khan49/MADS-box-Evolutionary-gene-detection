import os
import subprocess
from collections import defaultdict

NIPGR_WORK_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/NIPGR_WORK"
RESULTS_DIR = os.path.abspath("Results_v4")

SPECIES_LIST = [
    "Amborella_trichopoda",
    "Cinnamomum_kanehirae",
    "Glycine_max",
    "Helianthus_annuuss",
    "Medicago_truncatula",
    "Nelumbo_nucifera",
    "Nymphaea_colorata",
    "Oryza_sativa",  # Oryza_sativa is used as a standard species name, user says 'please use scientific names instead of rice'
    "Prunus_persica"
]
# Excluded Piper_auritum based on user instruction

def extract_domtblout_ids(domtblout_file):
    """Parses a domtblout file and returns a robust set of hitting gene IDs"""
    ids = set()
    if not os.path.exists(domtblout_file):
        return ids
    with open(domtblout_file, "r") as f:
        for line in f:
            if line.startswith("#"): continue
            parts = line.split()
            if len(parts) > 0:
                raw_id = parts[0]
                clean_id = raw_id.split("|")[0]
                ids.add(clean_id)
    return ids

def parse_fasta(fasta_file):
    """Returns a dictionary of sequences"""
    seqs = {}
    if not os.path.exists(fasta_file):
        return seqs
    current_header = ""
    current_seq = []
    with open(fasta_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if line.startswith(">"):
                if current_header:
                    seqs[current_header] = "".join(current_seq)
                raw_header = line.split()[0][1:]  # remove >
                current_header = raw_header.split("|")[0]
                current_seq = []
            else:
                current_seq.append(line)
    if current_header:
        seqs[current_header] = "".join(current_seq)
    return seqs

def generate_at_deligient_candidates():
    print("--- Phase 1: Generating AT_deligient_candidates ---")
    mads_file = os.path.join(NIPGR_WORK_DIR, "AT_MADS.domtblout")
    kbox_file = os.path.join(NIPGR_WORK_DIR, "AT_Kbox.domtblout")
    at_proteome = "/Users/bushrakhan/Desktop/NIPGR-data/TASK_4/Arabidopsis/Athaliana_clean.fa"
    
    mads_ids = extract_domtblout_ids(mads_file)
    kbox_ids = extract_domtblout_ids(kbox_file)
    
    intersect_ids = mads_ids.intersection(kbox_ids)
    print(f"AT MADS hits: {len(mads_ids)}, K-box hits: {len(kbox_ids)}")
    print(f"Intersection (AT Deligient Candidates): {len(intersect_ids)}")
    
    at_seqs = parse_fasta(at_proteome)
    
    out_file = os.path.join(RESULTS_DIR, "AT_deligient_candidates.fa")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    saved_count = 0
    with open(out_file, "w") as f:
        for seq_id in intersect_ids:
            if seq_id in at_seqs:
                f.write(f">{seq_id}\n{at_seqs[seq_id]}\n")
                saved_count += 1
                
    print(f"Saved {saved_count} AT candidates to {out_file}\n")
    return out_file

def run_msa(input_fa, out_mafft, out_muscle, out_clustalo):
    print("  -> Running Triple Alignment (MAFFT, MUSCLE, ClustalO)...")
    with open(out_mafft, "w") as f_out:
        subprocess.run(["mafft", "--auto", "--thread", "-1", input_fa], stdout=f_out, stderr=subprocess.DEVNULL)
        
    subprocess.run(["muscle", "-align", input_fa, "-output", out_muscle], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    subprocess.run(["clustalo", "-i", input_fa, "-o", out_clustalo, "--force", "--threads", "0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_iqtree(msa_file, prefix, method):
    treefile = prefix + ".treefile"
    if os.path.exists(treefile):
        print(f"  -> Skipping (already done): {os.path.basename(treefile)}")
        return
    # NJ: JTT+G fast fixed model. Bayes: LG+G fixed model (avoids slow MFP model search).
    # IQ-TREE requires minimum 1000 replicates for -B (Ultrafast Bootstrap).
    if method == "nj":
        cmd = ["iqtree2", "-s", msa_file, "-m", "JTT+G", "-B", "1000", "-T", "AUTO", "-pre", prefix, "-redo"]
    elif method == "abayes":
        cmd = ["iqtree2", "-s", msa_file, "-m", "LG+G", "-B", "1000", "-T", "AUTO", "--abayes", "-pre", prefix, "-redo"]
    else:
        return
        
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error running IQ-TREE for {prefix}: {e}")

def process_species(species, at_ref_file):
    print(f"\n--- Phase 2: Processing {species} ---")
    
    # As explicitly instructed: using the file produced in the earlier step
    species_cand_file = os.path.join(NIPGR_WORK_DIR, species, f"{species}_candidates.fa")
    if not os.path.exists(species_cand_file):
        print(f"  -> ERROR: {species_cand_file} not found. Ensure earlier steps completed successfully. Skipping.")
        return
        
    out_dir = os.path.join(RESULTS_DIR, species)
    os.makedirs(out_dir, exist_ok=True)
    
    merged_fa = os.path.join(out_dir, f"{species}_with_AT_aligned_input.fa")
    
    # Contextual merge: combine AT_deligient_candidates with species_deligient_candidates
    print("  -> Combining with AT_deligient_candidates...")
    if not os.path.exists(merged_fa):
        with open(merged_fa, "w") as out_f, open(species_cand_file, "r") as sp_f, open(at_ref_file, "r") as at_f:
            out_f.write(sp_f.read().strip() + "\n")
            out_f.write(at_f.read().strip() + "\n")
    else:
        print(f"  -> Skipping merge (already exists): {os.path.basename(merged_fa)}")
        
    mafft_out = os.path.join(out_dir, f"{species}_MAFFT.fa")
    muscle_out = os.path.join(out_dir, f"{species}_MUSCLE.fa")
    clustal_out = os.path.join(out_dir, f"{species}_ClustalO.fa")
    
    # Skip alignments if already done
    if all(os.path.exists(f) for f in [mafft_out, muscle_out, clustal_out]):
        print("  -> Skipping alignments (all 3 already exist).")
    else:
        run_msa(merged_fa, mafft_out, muscle_out, clustal_out)
    
    print("  -> Constructing NJ Trees (BIONJ)...")
    run_iqtree(mafft_out, os.path.join(out_dir, f"{species}_MAFFT_NJ"), "nj")
    run_iqtree(muscle_out, os.path.join(out_dir, f"{species}_MUSCLE_NJ"), "nj")
    run_iqtree(clustal_out, os.path.join(out_dir, f"{species}_ClustalO_NJ"), "nj")
    
    print("  -> Constructing Bayesian Trees (aBayes)...")
    run_iqtree(mafft_out, os.path.join(out_dir, f"{species}_MAFFT_Bayes"), "abayes")
    run_iqtree(muscle_out, os.path.join(out_dir, f"{species}_MUSCLE_Bayes"), "abayes")
    run_iqtree(clustal_out, os.path.join(out_dir, f"{species}_ClustalO_Bayes"), "abayes")
    
    print(f"[{species}] Construction complete.")

if __name__ == "__main__":
    print(f"Output directory: {RESULTS_DIR}")
    at_ref = generate_at_deligient_candidates()
    
    for sp in SPECIES_LIST:
        process_species(sp, at_ref)
        
    print("\n--- BATCH PROCESSING COMPLETE ---")
