import os
import glob
import subprocess
import shutil
from Bio import SeqIO

# --- CONFIGURATION ---
BASE_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection"
WORK_DIR = os.path.join(BASE_DIR, "Simultaneous_Phylogenetic_Analysis")
RESULTS_DIR = os.path.join(WORK_DIR, "Results_v3")
HMM_DIR = os.path.join(BASE_DIR, "Workflow_Step-by-Step/TASK_1/uploads")
ANCHORS_FILE = os.path.join(WORK_DIR, "Datasets/AT_Full_Anchors.fa")

HMM_MADS = os.path.join(HMM_DIR, "PF00319.MADS.hmm")
HMM_KBOX = os.path.join(HMM_DIR, "PF01486.K_domain.hmm")
HMM_AP2 = os.path.join(HMM_DIR, "PF00847.AP2.hmm")

os.makedirs(RESULTS_DIR, exist_ok=True)
TEMP_DIR = os.path.join(RESULTS_DIR, "temp_processing")

# --- UTILS ---
def run_cmd(cmd, cwd=None):
    print(f"Executing: {cmd}")
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error: {stderr.decode()}")
    return stdout.decode(), stderr.decode()

def get_ids_from_domtbl(tbl_path):
    ids = set()
    if not os.path.exists(tbl_path): return ids
    with open(tbl_path, "r") as f:
        for line in f:
            if line.startswith("#"): continue
            parts = line.split()
            if parts: ids.add(parts[0])
    return ids

def parse_blast_ids(blast_path):
    ids = set()
    if not os.path.exists(blast_path): return ids
    with open(blast_path, "r") as f:
        for line in f:
            if line.startswith("#"): continue
            parts = line.split()
            if parts: ids.add(parts[0]) # Assuming qseqid is first
    return ids

# --- PIPELINE ---
def process_species(task_id, species_name):
    print(f"\n>>> PROCESSING: {species_name} (TASK_{task_id}) <<<")
    species_results = os.path.join(RESULTS_DIR, species_name.replace(" ", "_"))
    os.makedirs(species_results, exist_ok=True)
    
    task_path = os.path.join(BASE_DIR, f"Workflow_Step-by-Step/TASK_{task_id}/uploads")
    if not os.path.exists(task_path):
        print(f"Warning: Task path {task_path} does not exist. Searching parent...")
        task_path = os.path.join(BASE_DIR, f"Workflow_Step-by-Step/TASK_{task_id}")

    # 1. Locate Proteome Zip and Blast Out
    zips = glob.glob(os.path.join(task_path, "*.zip"))
    blast_outs = glob.glob(os.path.join(task_path, "*.out"))
    
    if not zips:
        print(f"Failed: No proteome zip found in {task_path}")
        return
    
    # Use the largest zip as proteome
    proteome_zip = max(zips, key=os.path.getsize)
    print(f"Using proteome zip: {os.path.basename(proteome_zip)}")
    
    # Unzip
    if os.path.exists(TEMP_DIR): shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)
    run_cmd(f"unzip -o '{proteome_zip}' -d '{TEMP_DIR}'")
    
    # Find the unzipped FASTA
    fasta_files = glob.glob(os.path.join(TEMP_DIR, "*.fa")) + glob.glob(os.path.join(TEMP_DIR, "*.fasta"))
    if not fasta_files:
        print("Failed: No FASTA found after unzipping.")
        return
    proteome_fa = fasta_files[0]
    
    # 2. HMMER Search
    mads_tbl = os.path.join(TEMP_DIR, "mads.tbl")
    kbox_tbl = os.path.join(TEMP_DIR, "kbox.tbl")
    ap2_tbl = os.path.join(TEMP_DIR, "ap2.tbl")
    
    run_cmd(f"hmmsearch --domtblout '{mads_tbl}' '{HMM_MADS}' '{proteome_fa}'")
    run_cmd(f"hmmsearch --domtblout '{kbox_tbl}' '{HMM_KBOX}' '{proteome_fa}'")
    run_cmd(f"hmmsearch --domtblout '{ap2_tbl}' '{HMM_AP2}' '{proteome_fa}'")
    
    # 3. Logic Filtering
    mads_ids = get_ids_from_domtbl(mads_tbl)
    kbox_ids = get_ids_from_domtbl(kbox_tbl)
    ap2_ids = get_ids_from_domtbl(ap2_tbl)
    
    hmm_candidates = (mads_ids | kbox_ids) - ap2_ids
    print(f"HMM Candidates (MADS|Kbox - AP2): {len(hmm_candidates)}")
    
    # 4. Blast Intersection
    if blast_outs:
        blast_ids = parse_blast_ids(blast_outs[0])
        final_ids = hmm_candidates & blast_ids
        print(f"Intersection with Blast ({os.path.basename(blast_outs[0])}): {len(final_ids)}")
    else:
        print("Warning: No Blast output found. Skipping intersection.")
        final_ids = hmm_candidates
        
    if not final_ids:
        print("Failed: No candidates finalized.")
        return

    # 5. Extract sequences
    final_fasta = os.path.join(species_results, f"{species_name.replace(' ', '_')}_diligent.fa")
    records = []
    with open(proteome_fa, "r") as f:
        for rec in SeqIO.parse(f, "fasta"):
            if rec.id in final_ids:
                records.append(rec)
    SeqIO.write(records, final_fasta, "fasta")
    print(f"Final sequences saved to {final_fasta}")

    # 6. Phylogeny Pipeline
    # Combine with anchors
    merged_fa = os.path.join(species_results, "merged_with_AT.fa")
    with open(merged_fa, "w") as out:
        for rec in records: SeqIO.write(rec, out, "fasta")
        with open(ANCHORS_FILE, "r") as r: out.write(r.read())
        
    # triple MSA
    algos = ["mafft", "muscle", "clustalo"]
    for algo in algos:
        msa_fa = os.path.join(species_results, f"msa_{algo}.fa")
        if algo == "mafft": run_cmd(f"mafft --auto '{merged_fa}' > '{msa_fa}'")
        elif algo == "muscle": run_cmd(f"muscle -in '{merged_fa}' -out '{msa_fa}'")
        elif algo == "clustalo": run_cmd(f"clustalo -i '{merged_fa}' -o '{msa_fa}' --force")
        
        # Dual Trees
        methods = {"NJ": "BIONJ", "Bayes": "aBayes"}
        for m_name, m_val in methods.items():
            prefix = os.path.join(species_results, f"tree_{algo}_{m_name}")
            run_cmd(f"iqtree2 -s '{msa_fa}' -m {m_val} -B 500 -fast -pre '{prefix}' -redo")

    print(f"Successfully completed phylogeny for {species_name}")

# --- MAIN ---
SPECIES_MAP = {
    1: "Rice",
    2: "Amborella trichopoda",
    # 3: Arabidopsis (Anchors come from here anyway)
    4: "Cinnamomum kanehirae",
    5: "Glycine max",
    6: "Helianthus annuuss",
    7: "Medicago truncatula",
    8: "Nelumbo nucifera",
    9: "Nymphaea colorata",
    10: "Prunus persica",
    11: "Piper auritum"
}

if __name__ == "__main__":
    # Test with Rice first
    process_species(1, SPECIES_MAP[1])
